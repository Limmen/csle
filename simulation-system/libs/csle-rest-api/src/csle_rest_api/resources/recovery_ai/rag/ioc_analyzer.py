from typing import List, Tuple, Dict, Any
from csle_rest_api.resources.recovery_ai.rag.ioc_extractor import IOCExtractor
from csle_rest_api.resources.recovery_ai.rag.otx_lookup import OTXLookup


class IOCAnalyzer:

    @staticmethod
    def find_iocs(log_text: str) -> Tuple[List[str], List[str], List[str], List[str], List[str], List[str]]:
        """
        Extracts IOCs from log text.

        :param log_text: the log text
        :return: the list of IOCs
        """
        urls = IOCExtractor.extract_urls(log_text)
        ips = IOCExtractor.extract_ips(log_text)
        hostnames = IOCExtractor.extract_hostnames(log_text)
        domains = IOCExtractor.extract_domains(log_text)
        cves = IOCExtractor.extract_cves(log_text)
        nids = IOCExtractor.extract_nids(log_text)
        return (list(set(urls)), list(set(ips)), list(set(hostnames)), list(set(domains)), list(set(cves)),
                list(set(nids)))

    @staticmethod
    def analyze(urls: List[str], ips: List[str], hostnames: List[str], domains: List[str],
                cves: List[str], nids: List[str]) -> Dict[str, Any]:

        # results = {
        #     "urls": [(u, OTXLookup.lookup_url(u)) for u in urls],
        #     "ips": [(ip, OTXLookup.lookup_ip(ip)) for ip in ips],
        #     "hostnames": [(h, OTXLookup.lookup_hostname(h)) for h in hostnames],
        #     "domains": [(d, OTXLookup.lookup_domain(d)) for d in domains],
        #     "cves": [(cve, OTXLookup.lookup_cve(cve)) for cve in cves],
        #     "nids": nids
        # }
        results = {
            "urls": [],
            "ips": [],
            "hostnames": [],
            "domains": [],
            "cves": [(cve, OTXLookup.lookup_cve(cve)) for cve in cves],
            "nids": []
        }
        return results

    @staticmethod
    def enrich_logs(log_text: str, analysis: Dict[str, Any]) -> str:
        """
        Enriches a given log text with threat intelligence

        :param log_text: the log text to enrich
        :param analysis: the threat intelligence analysis
        :return: the enriched log text
        """
        enrichment_summary = []

        for ip, data in analysis["ips"]:
            pulse_info = data.get("pulse_info", {}).get("pulses", [])
            if pulse_info:
                enrichment_summary.append(f"IP {ip}: {', '.join(p['name'] for p in pulse_info)}")

        for domain, data in analysis["domains"]:
            pulse_info = data.get("pulse_info", {}).get("pulses", [])
            if pulse_info:
                enrichment_summary.append(f"Domain {domain}: {', '.join(p['name'] for p in pulse_info)}")

        for url, data in analysis["urls"]:
            pulse_info = data.get("pulse_info", {}).get("pulses", [])
            if pulse_info:
                enrichment_summary.append(f"URL {url}: {', '.join(p['name'] for p in pulse_info)}")

        for hostname, data in analysis["hostnames"]:
            pulse_info = data.get("pulse_info", {}).get("pulses", [])
            if pulse_info:
                enrichment_summary.append(f"Hostname {hostname}: {', '.join(p['name'] for p in pulse_info)}")

        for cve, data in analysis["cves"]:
            if "description" in data:
                enrichment_summary.append(f"CVE {cve}: {data['description']}")

        if not enrichment_summary:
            return log_text

        summary_text = "\n\n".join(enrichment_summary)
        return log_text + "\n\n" + summary_text
