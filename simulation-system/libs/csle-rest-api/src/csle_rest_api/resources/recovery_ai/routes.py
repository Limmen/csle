"""
Routes and sub-resources for the /recovery-ai resource
"""
from __future__ import annotations

from typing import Tuple, Dict, Any, Generator
from flask import Blueprint, Response, request, stream_with_context, jsonify
from peft import PeftModel, PeftConfig
import json
import random
import torch
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants
import csle_rest_api.util.rest_api_util as rest_api_util
from csle_common.logging.log import Logger
from csle_rest_api.resources.recovery_ai.prompts import Prompts
from csle_rest_api.resources.recovery_ai.recovery_ai_util import RecoveryAIUtil
from csle_common.metastore.metastore_facade import MetastoreFacade

recovery_ai_bp = Blueprint(
    api_constants.MGMT_WEBAPP.RECOVERY_AI_RESOURCE, __name__,
    url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.RECOVERY_AI_RESOURCE}")

try:
    config = MetastoreFacade.get_config(id=1)
    if config.recovery_ai:
        tokenizer, llm = RecoveryAIUtil.load_llm()
        output_dir = config.recovery_ai_output_dir
        peft_config = PeftConfig.from_pretrained(output_dir)
        assert isinstance(llm, torch.nn.Module)
        model = PeftModel.from_pretrained(llm, output_dir)
        model.eval()
        with open(config.recovery_ai_examples_path, "r") as f:
            examples = json.load(f)
except Exception as e:
    Logger.__call__().get_logger().warning(f"There was an exception loading LLM for RecoveryAI. "
                                           f"Exception: {str(e)}, {repr(e)}")


@recovery_ai_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def recovery_ai() -> Tuple[Response, int]:
    """
    SSE endpoint that streams tokens of the recovery plan
    """
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=False)
    if authorized is not None:
        return authorized
    body: Dict[str, Any] = request.get_json(silent=True) or {}
    system: str = body.get(api_constants.MGMT_WEBAPP.RECOVERY_AI_JSON_SYSTEM_DESCRIPTION, "")
    logs: str = body.get(api_constants.MGMT_WEBAPP.RECOVERY_AI_JSON_LOGS, "")
    rag: bool = body.get(api_constants.MGMT_WEBAPP.RECOVERY_AI_RAG, False)
    lookahead_horizon: int = body.get(api_constants.MGMT_WEBAPP.RECOVERY_AI_LOOKAHEAD_HORIZON, 1)
    rollout_horizon: int = body.get(api_constants.MGMT_WEBAPP.RECOVERY_AI_ROLLOUT_HORIZON, 1)
    optimization_steps: int = body.get(api_constants.MGMT_WEBAPP.RECOVERY_AI_OPTIMIZATION_STEPS, 1)
    temperature: float = body.get(api_constants.MGMT_WEBAPP.RECOVERY_AI_TEMPERATURE, 1.0)

    def llm_stream(logs: str, system: str) -> Generator[str, None, None]:
        if rag:
            rag_output = yield from RecoveryAIUtil.gemini_rag(logs=logs)
            if rag_output is None:
                raise ValueError("There was an exception generating Rag output")
            identifiers, contexts = rag_output
            logs = RecoveryAIUtil.enrich_logs(logs=logs, identifiers=identifiers, contexts=contexts)
        incident_input = RecoveryAIUtil.create_incident_prompt(system, logs, Prompts.INCIDENT_PROMPT_TEMPLATE)
        incident_classification = yield from RecoveryAIUtil.incident_classification(
            incident_input=incident_input, model=model, tokenizer=tokenizer, system=system, logs=logs,
            num_optimization_steps=optimization_steps, temperature=temperature, lookahead_horizon=lookahead_horizon,
            rollout_horizon=rollout_horizon)
        if incident_classification is None:
            raise ValueError("There was an exception classifying the incident")
        if incident_classification[Prompts.INCIDENT] == Prompts.INCIDENT_YES:
            incident_str = RecoveryAIUtil.format_incident_description(incident_classification)
            yield from RecoveryAIUtil.recovery_loop(model=model, tokenizer=tokenizer, system=system, logs=logs,
                                                    incident_str=incident_str,
                                                    action_prompt_template=Prompts.ACTION_PROMPT_TEMPLATE,
                                                    state_prompt_template=Prompts.STATE_PROMPT_TEMPLATE,
                                                    temperature=temperature, lookahead_horizon=lookahead_horizon,
                                                    rollout_horizon=rollout_horizon,
                                                    num_optimization_steps=optimization_steps)

    response = Response(
        stream_with_context(llm_stream(logs=logs, system=system)),
        status=constants.HTTPS.OK_STATUS_CODE,
        content_type=api_constants.MGMT_WEBAPP.EVENT_STREAM_CONTENT_TYPE,
    )
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
