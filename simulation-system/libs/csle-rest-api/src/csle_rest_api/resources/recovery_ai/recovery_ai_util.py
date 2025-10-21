import time
from typing import Tuple, Dict, List, Any, Generator, cast, Optional, Union
import os
from transformers import AutoTokenizer, AutoModelForCausalLM, PreTrainedModel
from transformers.tokenization_utils import PreTrainedTokenizer
from transformers.utils.quantization_config import BitsAndBytesConfig
from transformers.generation.streamers import TextIteratorStreamer
from peft import PeftModel
import torch
import json
import threading
from google import genai # type: ignore
import numpy as np
import re
from csle_common.logging.log import Logger
import csle_rest_api.constants.constants as api_constants
from csle_rest_api.resources.recovery_ai.rag.ioc_analyzer import IOCAnalyzer
from csle_rest_api.resources.recovery_ai.prompts import Prompts


class RecoveryAIUtil:

    @staticmethod
    def load_llm() -> Tuple[PreTrainedTokenizer, PreTrainedModel]:
        """
        Utility function for loading the pre-trained LLM from disk.

        :return: the loaded LLM as well as the corresponding tokenizer.
        """
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

    @staticmethod
    def is_state_terminal(state: Dict[str, bool]) -> bool:
        """
        Utility function that checks whether a given recovery state is terminal or not.

        :param state: the state to check
        :return: True if it is terminal, False otherwise
        """
        return (state[Prompts.IS_ATTACK_CONTAINED] and state[Prompts.IS_KNOWLEDGE_SUFFICIENT]
                and state[Prompts.ARE_FORENSICS_PRESERVED]
                and state[Prompts.IS_ERADICATED] and state[Prompts.IS_HARDENED] and state[Prompts.IS_RECOVERED])

    @staticmethod
    def generate_previous_actions_str(previous_actions: List[Dict[str, str]]) -> str:
        """
        Utility functions for formatting the list of previous recovery actions into a string suitable for a prompt.

        :param previous_actions: the list of previous recovery actions
        :return: the formatted string
        """
        if not previous_actions:
            return "None."
        return "\n".join([f"Action: {a[Prompts.ACTION]} Explanation: {a[Prompts.EXPLANATION]}"
                          for a in previous_actions])

    @staticmethod
    def generate_output(model: Union[PreTrainedModel, PeftModel], tokenizer: PreTrainedTokenizer, prompt: str,
                        no_think: bool = False, temperature: float = 0.6) \
            -> Generator[str, Any, Union[List[str], Tuple[str, str]]]:
        """
        Uses a given LLM, tokenizer, and prompt to generate a stream of outputs

        :param model: the pre-trained LLM
        :param tokenizer: the tokenizer
        :param prompt: the prompt
        :param no_think: boolean flag indicating whether to skip the <think> token.
        :param temperature: parameter that controls the stochasticity of the output (higher means more stochastic)
        :return: the reasoning string and the answer string by the LLM.
        """
        assert isinstance(model, torch.nn.Module)
        model.eval()
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        streamer = TextIteratorStreamer(cast(AutoTokenizer, tokenizer), skip_special_tokens=True, skip_prompt=True)
        thread = threading.Thread(target=model.generate,  # type: ignore
                                  kwargs={**inputs, "max_new_tokens": 6000, "temperature": temperature,
                                          "do_sample": True, "streamer": streamer})
        thread.start()
        output = ""
        for text in streamer:
            output = output + text
            if text != "":
                text = text.replace("\n", "\\n")
                if api_constants.MGMT_WEBAPP.RECOVERY_AI_THINK_END_DELIMITER in text:
                    split_parts = text.split(api_constants.MGMT_WEBAPP.RECOVERY_AI_THINK_END_DELIMITER, 1)
                    yield f"{api_constants.MGMT_WEBAPP.RECOVERY_AI_DATA_DELIMITER} {split_parts[0]} \\n\\n\n\n"
                    if not no_think:
                        yield (f"{api_constants.MGMT_WEBAPP.RECOVERY_AI_DATA_DELIMITER} "
                               f"{api_constants.MGMT_WEBAPP.RECOVERY_AI_THINK_END_DELIMITER}\n\n")
                else:
                    yield f"{api_constants.MGMT_WEBAPP.RECOVERY_AI_DATA_DELIMITER} {text}\n\n"
        return output.split("</think>", 1)

    @staticmethod
    def format_incident_description(incident: Dict[str, Any]) -> str:
        """
        Utility function for formatting an incident report as a string suitable as a prompt.

        :param incident: the incident report
        :return: the formatted string
        """
        description: str = incident[Prompts.INCIDENT_DESCRIPTION]
        description += "\nMITRE ATT&CK tactics being used: " + ", ".join(incident[Prompts.MITRE_ATTACK_TACTICS]) + "."
        description += "\nMITRE ATT&CK techniques being used: " + ", ".join(
            incident[Prompts.MITRE_ATTACK_TECHNIQUES]) + "."
        description += "\nAttacker IPs/hostnames identified: " + ", ".join(
            incident[Prompts.ENTITIES][Prompts.ATTACKER]) + "."
        description += "\nSystem IPs/hostnames identified: " + ", ".join(
            incident[Prompts.ENTITIES][Prompts.SYSTEM]) + "."
        description += "\nIPs/hostnames targeted by the attack: " + ", ".join(
            incident[Prompts.ENTITIES][Prompts.TARGETED]) + "."
        return description

    @staticmethod
    def create_incident_prompt(system: str, logs: str, template: str) -> str:
        """
        Utiltiy function for creating the incident prompt from the template given a system description
        and a logs description.
        :param system: the system description
        :param logs: the logs description
        :param template: the prompt template
        :return: the prompt
        """
        return template.format(system, logs)

    @staticmethod
    def otx_rag(logs: str) -> Generator[str, Any, str]:
        """
        Utility function for retrieval-augmented generation

        :param logs: the logs to enrich with retrieved infromation
        :return: the enriched logs
        """
        urls, ips, hostnames, domains, cves, nids = IOCAnalyzer.find_iocs(log_text=logs)
        num_iocs = len(urls) + len(ips) + len(hostnames) + len(domains) + len(cves) + len(nids)
        ioc_text = (f"Found {len(urls)} URLs, {len(ips)} IPs, {len(hostnames)} hostnames, {len(domains)} domains, "
                    f"{len(cves)} CVEs, and {len(nids)} NIDS in the logs.\\n\\n")
        tokens = ioc_text.split(" ")
        for i in range(len(tokens)):
            if i > 0:
                token = " " + tokens[i]
            yield f"{api_constants.MGMT_WEBAPP.RECOVERY_AI_DATA_DELIMITER} {token}\n\n"
        if num_iocs > 0:
            ioc_text = "Retrieving threat information...\\n\\n"
            tokens = ioc_text.split(" ")
            for token in tokens:
                for i in range(len(tokens)):
                    if i > 0:
                        token = " " + tokens[i]
                yield f"{api_constants.MGMT_WEBAPP.RECOVERY_AI_DATA_DELIMITER} {token}\n\n"
            threat_intel = None
            try:
                threat_intel = IOCAnalyzer.analyze(urls=urls, ips=ips, hostnames=hostnames, domains=domains, cves=cves,
                                                   nids=nids)
            except Exception:
                pass
            ioc_text = "Information retrieval complete.\\n\\n"
            tokens = ioc_text.split(" ")
            for token in tokens:
                yield f"{api_constants.MGMT_WEBAPP.RECOVERY_AI_DATA_DELIMITER} {token}\n\n"
            if threat_intel is not None:
                logs = IOCAnalyzer.enrich_logs(log_text=logs, analysis=threat_intel)
        return logs

    @staticmethod
    def recovery_loop(model: Union[PreTrainedModel, PeftModel], tokenizer: PreTrainedTokenizer, system: str, logs: str,
                      incident_str: str, action_prompt_template: str, state_prompt_template: str,
                      num_optimization_steps: int = 3, temperature: float = 1, lookahead_horizon: int = 1,
                      rollout_horizon: int = 1) -> Generator[str, None, None]:
        """
        Loop that generates the recovery plan from a given incident report.

        :param model: the LLM
        :param tokenizer: the tokenizer of the LLM
        :param system: the system description
        :param logs: the logs description
        :param incident_str: the incident report
        :param action_prompt_template:  the prompt template for generating actions
        :param state_prompt_template: the prompt template for generating states
        :param num_optimization_steps: the number of actions to evaluate before selecting one
        :param temperature: the temperature for action generation when num_optimization_steps > 1
        :param lookahead_horizon: the lookahead horizon for the action selection
        :param rollout_horizon: the rollout horizon for the action selection
        :return: None
        """
        state = {
            Prompts.IS_ATTACK_CONTAINED: False,
            Prompts.IS_KNOWLEDGE_SUFFICIENT: False,
            Prompts.ARE_FORENSICS_PRESERVED: False,
            Prompts.IS_ERADICATED: False,
            Prompts.IS_HARDENED: False,
            Prompts.IS_RECOVERED: False
        }
        previous_actions: List[Dict[str, str]] = []
        while not RecoveryAIUtil.is_state_terminal(state):
            previous_actions_str = RecoveryAIUtil.generate_previous_actions_str(previous_actions)
            action_input = action_prompt_template.format(system, logs, incident_str, json.dumps(state, indent=4),
                                                         previous_actions_str)
            action: Optional[Dict[str, str]] = yield from RecoveryAIUtil.action_selection(
                action_input=action_input, model=model, tokenizer=tokenizer, state=state,
                state_prompt_template=state_prompt_template, system=system, logs=logs, incident_str=incident_str,
                num_optimization_steps=num_optimization_steps)
            if action is None:
                raise ValueError("There was an error generating the action.")
            previous_actions.append(action)

            action_str = (f"{Prompts.ACTION}: {action[Prompts.ACTION]}\n{Prompts.EXPLANATION}: "
                          f"{action[Prompts.EXPLANATION]}")
            state_input = state_prompt_template.format(system, logs, incident_str, json.dumps(state, indent=4),
                                                       action_str)
            _, state_output_str = yield from RecoveryAIUtil.generate_output(model, tokenizer, state_input)
            state = json.loads(state_output_str)
        return None

    @staticmethod
    def gemini_rag(logs: str) -> Generator[str, Any, Union[None, Tuple[list[Any], list[Any]], Tuple[Any, Any]]]:
        """
        Retrieves information abut threat identifiers in the logs/system description.

        :param logs: the logs
        :return: a list of threat identifiers and a list of contexts for those identifiers
        """
        urls, ips, hostnames, domains, cves, nids = IOCAnalyzer.find_iocs(log_text=logs)
        ioc_text = (f"Found {len(urls)} URLs, {len(ips)} IPs, {len(hostnames)} hostnames, {len(domains)} domains, "
                    f"{len(cves)} CVEs, and {len(nids)} NIDS in the logs.\\n\\n"
                    f"Retrieving information about threat identifiers in the logs...\\n\\n")
        tokens = ioc_text.split(" ")
        for i in range(len(tokens)):
            token = tokens[i]
            if i > 0:
                token = " " + tokens[i]
            time.sleep(0.05)
            yield f"{api_constants.MGMT_WEBAPP.RECOVERY_AI_DATA_DELIMITER} {token}\n\n"

        instruction = Prompts.RAG_PROMPT_TEMPLATE.format(logs)
        api_key = os.environ.get(api_constants.RAG.GEMINI_API_KEY)
        if not api_key:
            raise ValueError(f"{api_constants.RAG.GEMINI_API_KEY} environment variable is not set")
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(model=api_constants.RAG.MODEL, contents=instruction)
        if response is None or response.text is None:
            raise ValueError("There was an error generating the response.")
        try:
            json_str = response.text.replace("```json\n", "")
            json_str = json_str.replace("```", "")
            response_json = json.loads(json_str)
            if api_constants.RAG.IDENTIFIERS in response_json and api_constants.RAG.CONTEXT in response_json:
                identifiers = response_json[api_constants.RAG.IDENTIFIERS]
                contexts = response_json[api_constants.RAG.CONTEXT]
                rag_str = ""
                for idx in range(min(len(identifiers), len(contexts))):
                    rag_str += f"Identifier: {identifiers[idx]}.\\n Retrieved information: {contexts[idx]}\\n\\n"
                rag_str += "\\n"
                tokens = rag_str.split(" ")
                for i in range(len(tokens)):
                    token = tokens[i]
                    if i > 0:
                        token = " " + tokens[i]
                    time.sleep(0.05)
                    yield f"{api_constants.MGMT_WEBAPP.RECOVERY_AI_DATA_DELIMITER} {token}\n\n"
                return identifiers, contexts
        except Exception as e:
            Logger.__call__().get_logger().warning(f"RAG exception: {str(e)}, {repr(e)}.")
            return [], []
        return None

    @staticmethod
    def enrich_logs(logs: str, identifiers: List[str], contexts: List[str]) -> str:
        """
        Enriches the logs with context about therat identifiers

        :param logs: the logs to enrich
        :param identifiers: the identifiers to provide contexts for
        :param contexts: the contexts for the identifiers
        :return: the enriched logs
        """
        context_str = ""
        for i in range(min(len(identifiers), len(contexts))):
            context_str += f"The meaning of the identifier: '{identifiers[i]}' is: {contexts[i]}\n"
        enriched_logs = logs + "\n" + context_str
        return enriched_logs

    @staticmethod
    def action_selection(action_input: str, model: Union[PreTrainedModel, PeftModel], tokenizer: PreTrainedTokenizer,
                         state: Dict[str, bool], state_prompt_template: str, system: str, logs: str,
                         incident_str: str, num_optimization_steps: int = 3, temperature: float = 1,
                         lookahead_horizon: int = 1, rollout_horizon: int = 1) \
            -> Generator[str, Any, Union[None, Dict[str, str]]]:
        """
        Lookahead optimization to select the next action to perform.

        :param action_input: the action prompt
        :param model: the LLM
        :param tokenizer: the tokenizer of the LLM
        :param state: the current state
        :param state_prompt_template: the prompt template for the state
        :param system: the system description
        :param logs: the logs
        :param incident_str: description of the incident
        :param num_optimization_steps: the number of actions to evaluate before selecting the next action
        :param temperature: the temperature for action generation when num_optimization_steps > 1
        :param lookahead_horizon: the lookahead horizon for the action selection
        :param rollout_horizon: the rollout horizon for the action selection
        :return:
        """
        if num_optimization_steps == 1:
            _, action_output_str = yield from RecoveryAIUtil.generate_output(model, tokenizer, action_input,
                                                                             no_think=False)
            action: Dict[str, str] = json.loads(action_output_str)
            return action

        candidate_actions: List[Dict[str, str]] = []
        rewards = []
        for i in range(num_optimization_steps):
            for token in f"Evaluating action {i + 1}/{num_optimization_steps}":
                time.sleep(0.05)
                yield f"{api_constants.MGMT_WEBAPP.RECOVERY_AI_DATA_DELIMITER} {token}\n\n"
            yield f"{api_constants.MGMT_WEBAPP.RECOVERY_AI_DATA_DELIMITER} \\n\n\n"
            if i == 0:
                temp = 0.6
            else:
                temp = temperature
            _, action_output_str = yield from RecoveryAIUtil.generate_output(
                model, tokenizer, action_input, no_think=True, temperature=temp)
            yield f"{api_constants.MGMT_WEBAPP.RECOVERY_AI_DATA_DELIMITER} \\n\n\n"
            for token in "The expected reward of taking this action is..  ":
                time.sleep(0.05)
                yield f"{api_constants.MGMT_WEBAPP.RECOVERY_AI_DATA_DELIMITER} {token}\n\n"

            action = json.loads(action_output_str)
            # action_str = (f"{Prompts.ACTION}: {action[Prompts.ACTION]}\n{Prompts.EXPLANATION}: "
            #               f"{action[Prompts.EXPLANATION]}")
            # state_input = state_prompt_template.format(system, logs, incident_str, json.dumps(state, indent=4),
            #                                            action_str)
            # _, state_output_str = yield from RecoveryAIUtil.generate_output(model, tokenizer, state_input, no_think
            # =False)
            # new_state = json.loads(state_output_str)
            # reward = 0
            # for k, v in new_state.items():
            #     if new_state[k] and not state[k]:
            #         reward += 1
            #     if state[k] and not new_state[k]:
            #         reward -= 1
            reward = 0.0

            try:
                api_key = os.environ.get(api_constants.RAG.GEMINI_API_KEY)
                client = genai.Client(api_key=api_key)
                instruction = Prompts.GEMINI_ACTION_EVAL.format(system, logs, incident_str,
                                                                json.dumps(state, indent=4), action[Prompts.ACTION])
                response = client.models.generate_content(model=api_constants.RAG.MODEL, contents=instruction)
                if response is None or response.text is None:
                    raise ValueError("Failed to generate response")
                response_score = float(response.text.strip())
                reward += response_score
            except Exception:
                pass
            rewards.append(reward)
            candidate_actions.append(action)
            for token in f"{reward}.":
                time.sleep(0.05)
                yield f"{api_constants.MGMT_WEBAPP.RECOVERY_AI_DATA_DELIMITER} {token}\n\n"
            yield f"{api_constants.MGMT_WEBAPP.RECOVERY_AI_DATA_DELIMITER} \\n\\n\n\n"
        selected_action_idx = np.argmax(rewards)
        for token in (f"I choose action {selected_action_idx + 1} since it yields the highest expected "
                      f"reward, namely {rewards[selected_action_idx]}."):
            time.sleep(0.05)
            yield f"{api_constants.MGMT_WEBAPP.RECOVERY_AI_DATA_DELIMITER} {token}\n\n"
        yield f"{api_constants.MGMT_WEBAPP.RECOVERY_AI_DATA_DELIMITER} \\n\\n\n\n"
        selected_action = candidate_actions[selected_action_idx]
        yield (f"{api_constants.MGMT_WEBAPP.RECOVERY_AI_DATA_DELIMITER} "
               f"{api_constants.MGMT_WEBAPP.RECOVERY_AI_THINK_END_DELIMITER}\n\n")
        selected_action_str = json.dumps(selected_action, indent=4)
        selected_action_str = selected_action_str.replace("\n", "\\n")
        tokens = re.findall(r'\\n|.', selected_action_str)
        for token in tokens:
            time.sleep(0.05)
            yield f"{api_constants.MGMT_WEBAPP.RECOVERY_AI_DATA_DELIMITER} {token}\n\n"
        return candidate_actions[selected_action_idx]

    @staticmethod
    def incident_classification(incident_input: str, model: Union[PreTrainedModel, PeftModel],
                                tokenizer: PreTrainedTokenizer,
                                system: str, logs: str, num_optimization_steps: int = 3, temperature: float = 1,
                                lookahead_horizon: int = 1, rollout_horizon: int = 1) \
            -> Generator[str, Any, Union[None, Dict[str, str]]]:
        """
        Lookahead optimization to classify the incident

        :param incident_input: the incident prompt
        :param model: the LLM
        :param tokenizer: the tokenizer of the LLM
        :param system: the system description
        :param logs: the logs
        :param num_optimization_steps: the number of incident classification to evaluate before selecting one
        :param temperature: the temperature for incident classification generation when num_optimization_steps > 1
        :param lookahead_horizon: the lookahead horizon for the incident classification selection
        :param rollout_horizon: the rollout horizon for the incident classification selection
        :return:
        """
        _, incident_output_str = yield from RecoveryAIUtil.generate_output(model, tokenizer, incident_input)
        incident_classification: Dict[str, str] = json.loads(incident_output_str)
        return incident_classification
        # if num_optimization_steps == 1:
        #     _, incident_output_str = yield from RecoveryAIUtil.generate_output(model, tokenizer, incident_input)
        #     incident_classification = json.loads(incident_output_str)
        #     return incident_classification

        # candidate_classifications = []
        # rewards = []
        # for i in range(num_optimization_steps):
        #     for token in f"Evaluating incident classification {i + 1}/{num_optimization_steps}":
        #         time.sleep(0.05)
        #         yield f"{api_constants.MGMT_WEBAPP.RECOVERY_AI_DATA_DELIMITER} {token}\n\n"
        #     yield f"{api_constants.MGMT_WEBAPP.RECOVERY_AI_DATA_DELIMITER} \\n\\n\n\n"
        #     if i == 0:
        #         temp = 0.6
        #     else:
        #         temp = temperature
        #     _, incident_output_str = yield from RecoveryAIUtil.generate_output(
        #         model, tokenizer, incident_input, no_think=True, temperature=temp)
        #     yield f"{api_constants.MGMT_WEBAPP.RECOVERY_AI_DATA_DELIMITER} \\n\n\n"
        #     for token in "The expected reward of this incident classification is..  ":
        #         time.sleep(0.05)
        #         yield f"{api_constants.MGMT_WEBAPP.RECOVERY_AI_DATA_DELIMITER} {token}\n\n"
        #
        #     incident_classification = json.loads(incident_output_str)
        #     incident_str = incident_classification[Prompts.INCIDENT_DESCRIPTION]
        #     reward = 0
        #     try:
        #         api_key = os.environ.get(api_constants.RAG.GEMINI_API_KEY)
        #         client = genai.Client(api_key=api_key)
        #         instruction = Prompts.GEMINI_INCIDENT_EVAL.format(system, logs, incident_str)
        #         response = client.models.generate_content(model=api_constants.RAG.MODEL, contents=instruction)
        #         response_score = float(response.text.strip())
        #         reward += response_score
        #     except Exception:
        #         pass
        #     rewards.append(reward)
        #     candidate_classifications.append(incident_classification)
        #     for token in f"{reward}.":
        #         time.sleep(0.05)
        #         yield f"{api_constants.MGMT_WEBAPP.RECOVERY_AI_DATA_DELIMITER} {token}\n\n"
        #     yield f"{api_constants.MGMT_WEBAPP.RECOVERY_AI_DATA_DELIMITER} \\n\\n\n\n"
        # selected_incident_idx = np.argmax(rewards)
        # for token in (
        #         f"I choose incident classification {selected_incident_idx + 1} since it yields the highest expected "
        #         f"reward, namely {rewards[selected_incident_idx]}."):
        #     time.sleep(0.05)
        #     yield f"{api_constants.MGMT_WEBAPP.RECOVERY_AI_DATA_DELIMITER} {token}\n\n"
        # yield f"{api_constants.MGMT_WEBAPP.RECOVERY_AI_DATA_DELIMITER} \\n\\n\n\n"
        # selected_incident = candidate_classifications[selected_incident_idx]
        #
        # yield (f"{api_constants.MGMT_WEBAPP.RECOVERY_AI_DATA_DELIMITER} "
        #        f"{api_constants.MGMT_WEBAPP.RECOVERY_AI_THINK_END_DELIMITER}\n\n")
        # selected_incident_str = json.dumps(selected_incident, indent=4)
        # selected_incident_str = selected_incident_str.replace("\n", "\\n")
        # tokens = re.findall(r'\\n|.', selected_incident_str)
        # for token in tokens:
        #     time.sleep(0.05)
        #     yield f"{api_constants.MGMT_WEBAPP.RECOVERY_AI_DATA_DELIMITER} {token}\n\n"
        # return candidate_classifications[selected_incident_idx]
