from charmhelpers.core import hookenv
from charms.reactive import hook
from charms.reactive import RelationBase
from charms.reactive import scopes

class GitProvides(RelationBase):
    scope = scopes.SERVICE

    @hook('{provides:git}-relation-{joined,changed}')
    def changed(self):
        if self.get_remote('username') is not None:
            self.set_state('{relation_name}.username.available')
        if self.get_remote('public-key') is not None:
            self.set_state('{relation_name}.public-key.available')
        self.set_state('{relation_name}.available')

    @hook('{provides:git}-relation-departed')
    def departed(self):
        self.remove_state('{relation_name}.available')

    def configure(self, repo_path, protocols=["ssh"]):
        relation_info = {
            'hostname': hookenv.unit_get('private-address'),
            'protocols': protocols,
            'repo-path': repo_path,
        }
        self.set_remote(**relation_info)

