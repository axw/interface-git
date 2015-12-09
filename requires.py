from charmhelpers.core import hookenv
from charms.reactive import hook
from charms.reactive import RelationBase
from charms.reactive import scopes

class GitRequires(RelationBase):
    scope = scopes.SERVICE


    @hook('{requires:git}-relation-joined')
    def joined(self):
        self.set_state('{relation_name}.related')
        self.changed()


    @hook('{requires:git}-relation-changed')
    def changed(self):
        protocol = self.get_remote('protocol')
        if not protocol:
            return
        if not self.get_local('username'):
            # client has not called configure yet
            return
        required = ['hostname', 'repo-path']
        if protocol == 'ssh':
            required.append('ssh-host-key')
        if all(map(self.get_remote, required)):
            self.set_state('{relation_name}.available')

        local_commit = self.get_local('git-commit')
        remote_commit = self.get_remote('git-commit')
        if remote_commit and remote_commit != local_commit:
            self.set_state('{relation_name}.commit.changed')


    @hook('{requires:git}-relation-departed')
    def departed(self):
        self.remove_state('{relation_name}.available')
        self.remove_state('{relation_name}.related')


    def configure(self, username, public_key=None):
        relation_info = {
            'username': username,
        }
        if public_key is not None:
            relation_info['ssh-public-key'] = public_key
        self.set_local(username=username)
        self.set_remote(**relation_info)

 
    def set_commit(self, sha):
        self.set_local('git-commit', sha)
        if self.get_remote('git-commit') == sha:
            self.remove_state('{relation_name}.commit.changed')


    def url(self):
        # TODO(axw) decide URL based on protocol
        data = {
            'hostname':  self.get_remote('hostname'),
            'repo-path': self.get_remote('repo-path'),
            'username':  self.get_local('username'),
        }
        if all(data.values()):
            return str.format('{username}@{hostname}:{repo-path}', **data)
        return None
