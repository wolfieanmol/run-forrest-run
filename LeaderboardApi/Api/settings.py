from dataclasses import dataclass


@dataclass
class Name:
    domain: str
    name: str
    kind: str

    @property
    def full(self):
        return "".join(i.title() for i in (self.domain, self.name, self.kind))


name = Name(domain="google", name="accounts", kind="api")
port = 4700
version = "v1"


def version_endpoint_payload():
    return {"name": name.full, "version": version}