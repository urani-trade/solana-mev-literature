from dns.exception import DNSException
import dns.resolver
import dns.rdatatype


def resolve_cname(hostname):
    """Resolve a CNAME record to the original hostname.

    This is required for AWS where the hostname of the RDS instance is part of
    the signing request.

    """
    try:
        answers = dns.resolver.query(hostname, "CNAME")
        for answer in answers:
            if answer.rdtype == dns.rdatatype.CNAME:
                return answer.to_text().strip('.')
    except DNSException:
        return hostname
