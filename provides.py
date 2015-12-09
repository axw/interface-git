from charmhelpers.core import hookenv
from charms.reactive import hook
from charms.reactive import RelationBase
from charms.reactive import scopes

class GitProvides(RelationBase):
    scope = scopes.SERVICE


    @hook('{provides:git}-relation-{joined,changed}')
    def changed(self):
        self.set_state('{relation_name}.available')
        if self.get_remote('username') and self.get_remote('ssh-public-key'):
            self.set_state('{relation_name}.client.ready')


    @hook('{provides:git}-relation-departed')
    def departed(self):
        self.remove_state('{relation_name}.available')


    def configure(self, repo_path, ssh_host_key=None, protocol='ssh'):
        relation_info = {
            'hostname':  hookenv.unit_get('private-address'),
            'protocol':  protocol,
            'repo-path': repo_path,
        }
        if protocol == 'ssh':
            assert ssh_host_key
            relation_info['ssh-host-key'] = ssh_host_key
        self.set_remote(**relation_info)


    def set_commit(self, sha):
        self.set_remote('git-commit', sha)
