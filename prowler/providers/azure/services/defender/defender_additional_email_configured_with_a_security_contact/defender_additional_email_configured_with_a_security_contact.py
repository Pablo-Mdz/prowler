import re

from prowler.lib.check.models import Check, Check_Report_Azure
from prowler.providers.azure.services.defender.defender_client import defender_client


class defender_additional_email_configured_with_a_security_contact(Check):
    def execute(self) -> Check_Report_Azure:
        findings = []

        for (
            subscription_name,
            security_contacts,
        ) in defender_client.security_contacts.items():
            for contact in security_contacts.values():
                report = Check_Report_Azure(metadata=self.metadata(), resource=contact)
                report.status = "PASS"
                report.subscription = subscription_name
                report.status_extended = f"There is another correct email configured for subscription {subscription_name}."

                emails = contact.emails.split(";")

                for email in emails:
                    if re.fullmatch(
                        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", email
                    ):
                        break
                else:
                    report.status = "FAIL"
                    report.status_extended = f"There is not another correct email configured for subscription {subscription_name}."

                findings.append(report)

        return findings
