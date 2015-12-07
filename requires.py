from charmhelpers.core import hookenv
from charms.reactive import hook
from charms.reactive import RelationBase
from charms.reactive import scopes

class GitRequires(RelationBase):
    scope = scopes.SERVICE


    @hook('{provides:git}-relation-{joined,changed}')
    def changed(self):
        hostname = self.get_remote('hostname')
        if hostname is None:
            return
        repo_path = self.get_remote('repo-path')
        if repo_path is None:
            return
        if self.get_remote('hostname') and self.get_remote('port'):
            self.set_state('{relation_name}.available')


    @hook('{provides:git}-relation-{departed,broken}')
    def departed(self):
        self.remove_state('{relation_name}.available')


    def configure(self, username, public_key=None):
        relation_info = {
            'username': username,
        }
        if public_key is not None:
            relation_info['public-key'] = public_key
        self.set_local(username=username)
        self.set_remote(**relation_info)


    def url(self):
        data = {
            'hostname':  self.get_remote('hostname'),
            'repo-path': self.get_remote('repo-path'),
            'username':  self.get_local('username'),
        }
        if all(data.values()):
            return str.format('{username}@{hostname}:{repo-path}', **data)
        return None

