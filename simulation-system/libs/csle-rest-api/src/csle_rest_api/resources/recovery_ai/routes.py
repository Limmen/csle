"""
Routes and sub-resources for the /recovery-ai resource
"""
from __future__ import annotations

from typing import Tuple, Dict, Any, Generator
from flask import Blueprint, Response, request, stream_with_context, jsonify
from transformers import (AutoTokenizer, AutoModelForCausalLM, PreTrainedTokenizer, PreTrainedModel,
                          BitsAndBytesConfig)
from peft import PeftModel, PeftConfig
from transformers import TextIteratorStreamer
import threading
import torch
import json
import random
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants
import csle_rest_api.util.rest_api_util as rest_api_util
from csle_common.logging.log import Logger
from csle_rest_api.resources.recovery_ai.rag.ioc_analyzer import IOCAnalyzer

recovery_ai_bp = Blueprint(
    api_constants.MGMT_WEBAPP.RECOVERY_AI_RESOURCE, __name__,
    url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.RECOVERY_AI_RESOURCE}")


def load_llm() -> Tuple[PreTrainedTokenizer, PreTrainedModel]:
    tokenizer = AutoTokenizer.from_pretrained(api_constants.LLM.DEEPSEEK_14B_QWEN, use_fast=True)
    tokenizer.pad_token = tokenizer.eos_token
    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type=api_constants.LLM.NF4,
        bnb_4bit_compute_dtype=torch.bfloat16,
    )
    llm = AutoModelForCausalLM.from_pretrained(api_constants.LLM.DEEPSEEK_14B_QWEN,
                                               device_map={"": 0},
                                               quantization_config=quantization_config,
                                               attn_implementation=api_constants.LLM.SDPA,
                                               torch_dtype=torch.bfloat16)
    llm.use_memory_efficient_attention = True
    return tokenizer, llm


try:
    tokenizer, llm = load_llm()
    output_dir = "/home/kim/h300/checkpoint-525"
    peft_config = PeftConfig.from_pretrained(output_dir)
    model = PeftModel.from_pretrained(llm, output_dir)
    model.eval()
    with open("/home/kim/examples.json", "r") as f:
        examples = json.load(f)
except Exception as e:
    Logger.__call__().get_logger().warning(f"There was an exception loading LLM for RecoveryAI. "
                                           f"Exception: {str(e)}, {repr(e)}")


@recovery_ai_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def recovery_ai() -> Tuple[Response, int]:
    """
    SSE endpoint that streams tokens of the recovery plan (dummy implementation).

    For **POST** requests the client must send JSON of the form

    ```json
    {
      "systemDescription": "...",
      "networkLogs": "..."
    }
    ```

    A valid session token is still supplied as `?token=<JWT>` query parameter.
    """
    authorized = rest_api_util.check_if_user_is_authorized(
        request=request, requires_admin=False
    )
    if authorized is not None:
        return authorized
    body: Dict[str, Any] = request.get_json(silent=True) or {}
    system_description: str = body.get(api_constants.MGMT_WEBAPP.RECOVERY_AI_JSON_SYSTEM_DESCRIPTION, "")
    network_logs: str = body.get(api_constants.MGMT_WEBAPP.RECOVERY_AI_JSON_LOGS, "")
    prompt = (
        f"Below is a system description, a sequence of network logs (e.g., from an intrusion detection system), "
        f"and an instruction that describes a task.\n"
        f"Write a response that appropriately completes the request.\nBefore generating the response, "
        f"think carefully about the system, the logs, and the instruction, then create a step-by-step "
        f"chain of thoughts to ensure a logical and accurate response.\n\n"
        "### System:\n{}\n\n"
        "### Logs:\n{}\n\n"
        "### Instruction:\n"
        "You are a security operator with advanced knowledge in cybersecurity "
        f"and IT systems. You are monitoring alerts from an intrusion detection system and should"
        f" generate a plan with actions for recovering the system or explain why no recovery is needed. "
        f"Your suggested actions or (no action) should be based on the logs and the system description only.\n"
        "The recovery plan should be a valid JSON object with the keys: 'Incident', 'Incident description', "
        "'MITRE ATT&CK Tactics', 'MITRE ATT&CK Techniques', 'Recovery actions', "
        "and 'Action explanations'.\nThe 'Incident' entry should be either 'Yes' or 'No' if the Snort logs do "
        "not indicate an incident.\nThe 'Incident description' entry should describe the incident. "
        "If there is no incident, "
        "describe why that is the case.\nThe entries 'MITRE ATT&CK Tactics' and 'MITRE ATT&CK Techniques' "
        "should be arrays (empty if no incident) "
        "with tactics and techniques that the attacker used. The entries 'Recovery actions' "
        "and 'Action explanations' should be arrays (empty if no incident) that contain concrete and actionable recovery "
        "actions and explanations for why those actions are effective.\n"
        "If the logs/system description indicate an incident (i.e., Incident='Yes') but the logs "
        "are too vague to determine effective recovery actions, "
        "mention that and list actions for gathering more information. Don't make guesses, just state recovery actions "
        "based on what you know and mention further information that should be gathered. If Incident='No', then "
        "the list of recovery actions as well as the MITRE lists should be empty. If the logs contain information "
        "that is irrelevant to security, treat it as 'Incident'='No', don't guess. \n"
        "Make sure that the recovery plan is consistent with the system description and the logs. All conclusions in the"
        "recovery plan should be supported by the evidence in the system description or the logs.\n"
        "The goal when designing the recovery plan are: preserve evidence, stop the attack safely, "
        "minimize disruption, restore service, and block repeated attacks. The recovery actions should "
        "avoid unnecessary steps and follow the order: contain → eradicate → recover → harden. The recovery actions  "
        "should be concrete and actionable, avoid vague and repeated actions.\n\n"
        "### Response:\n<think>")

    gen_kwargs = dict(max_new_tokens=6000, temperature=0.6, do_sample=True)
    streamer = TextIteratorStreamer(tokenizer, skip_special_tokens=True, skip_prompt=True)
    urls, ips, hostnames, domains, cves, nids = IOCAnalyzer.find_iocs(log_text=network_logs)
    num_iocs = len(urls) + len(ips) + len(hostnames) + len(domains) + len(cves) + len(nids)

    def llm_stream(network_logs) -> Generator[str, None, None]:
        ioc_text = (f"Found {len(urls)} URLs, {len(ips)} IPs, {len(hostnames)} hostnames, {len(domains)} domains, "
                    f"{len(cves)} CVEs, and {len(nids)} NIDS in the logs.\\n\\n")
        tokens = ioc_text.split(" ")
        for token in tokens:
            yield f"{api_constants.MGMT_WEBAPP.RECOVERY_AI_DATA_DELIMITER} {token}\n\n"
        if num_iocs > 0:
            ioc_text = "Retrieving threat information...\\n\\n"
            tokens = ioc_text.split(" ")
            for token in tokens:
                yield f"{api_constants.MGMT_WEBAPP.RECOVERY_AI_DATA_DELIMITER} {token}\n\n"
            threat_intel = None
            try:
                threat_intel = IOCAnalyzer.analyze(urls=urls, ips=ips, hostnames=hostnames, domains=domains, cves=cves,
                                                   nids=nids)
            except:
                pass
            ioc_text = f"Information retrieval complete.\\n\\n"
            tokens = ioc_text.split(" ")
            for token in tokens:
                yield f"{api_constants.MGMT_WEBAPP.RECOVERY_AI_DATA_DELIMITER} {token}\n\n"
            if threat_intel is not None:
                network_logs = IOCAnalyzer.enrich_logs(log_text=network_logs, analysis=threat_intel)
        instruction = prompt.format(system_description, network_logs)
        inputs = tokenizer(instruction, return_tensors="pt").to(model.device)
        thread = threading.Thread(target=model.generate, kwargs={**inputs, **gen_kwargs, "streamer": streamer})
        thread.start()
        ioc_text = "Starting analysis..."
        tokens = ioc_text.split(" ")
        for token in tokens:
            yield f"{api_constants.MGMT_WEBAPP.RECOVERY_AI_DATA_DELIMITER} {token}\n\n"
        for new_text in streamer:
            if new_text != "":
                if api_constants.MGMT_WEBAPP.RECOVERY_AI_THINK_END_DELIMITER in new_text:
                    split_parts = new_text.split(api_constants.MGMT_WEBAPP.RECOVERY_AI_THINK_END_DELIMITER, 1)
                    yield f"{api_constants.MGMT_WEBAPP.RECOVERY_AI_DATA_DELIMITER} {split_parts[0]}\n\n"
                    yield f"{api_constants.MGMT_WEBAPP.RECOVERY_AI_DATA_DELIMITER} {api_constants.MGMT_WEBAPP.RECOVERY_AI_THINK_END_DELIMITER}\n\n"
                else:
                    yield f"{api_constants.MGMT_WEBAPP.RECOVERY_AI_DATA_DELIMITER} {new_text}\n\n"

    def no_answer_stream() -> Generator[str, None, None]:
        response = (
            'Step 1. The logs contain no substantial information, which means that no incident can be inferred. '
            '</think> {"Incident": "No", '
            '"Incident description": "No incident can be inferred from the logs because they contain'
            ' no substantial information.", "MITRE ATT&CK Tactics": [], "MITRE ATT&CK Techniques": [], '
            '"Recovery actions": [], "Action explanations": []}')
        tokens = response.split(" ")
        for token in tokens:
            yield f"{api_constants.MGMT_WEBAPP.RECOVERY_AI_DATA_DELIMITER} {token}\n\n"

    not_enough_information = False
    if network_logs.strip() == "" or network_logs.strip().lower() == "unknown" or network_logs.strip() == "-":
        not_enough_information = True

    if not not_enough_information:
        response = Response(
            stream_with_context(llm_stream(network_logs=network_logs)),
            status=constants.HTTPS.OK_STATUS_CODE,
            content_type=api_constants.MGMT_WEBAPP.EVENT_STREAM_CONTENT_TYPE,
        )
    else:
        response = Response(
            stream_with_context(no_answer_stream()),
            status=constants.HTTPS.OK_STATUS_CODE,
            content_type=api_constants.MGMT_WEBAPP.EVENT_STREAM_CONTENT_TYPE,
        )
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


@recovery_ai_bp.route("/example", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET])
def example() -> Tuple[Response, int]:
    """
    The /recovery-ai/example resource.

    :return: An example system description and log
    """
    requires_admin = False
    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
        requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized
    example = random.choice(examples)
    example_dict = {api_constants.MGMT_WEBAPP.RECOVERY_AI_JSON_SYSTEM_DESCRIPTION: example["System"],
                    api_constants.MGMT_WEBAPP.RECOVERY_AI_JSON_LOGS: "\n".join(example["Logs"])}
    response = jsonify(example_dict)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE
