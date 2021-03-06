from uuid import uuid4

from changes.config import db
from changes.constants import Status
from changes.models import TestGroup
from changes.testutils import APITestCase


class BuildTestIndexTest(APITestCase):
    def test_simple(self):
        fake_id = uuid4()

        build = self.create_build(self.project)
        job = self.create_job(build, status=Status.finished)

        group = TestGroup(
            job=job,
            project=self.project,
            name='foo',
            name_sha='a' * 40,
        )
        db.session.add(group)

        path = '/api/0/builds/{0}/tests/'.format(fake_id.hex)

        resp = self.client.get(path)
        assert resp.status_code == 404

        path = '/api/0/builds/{0}/tests/'.format(build.id.hex)

        resp = self.client.get(path)
        assert resp.status_code == 200
        data = self.unserialize(resp)
        assert len(data) == 1
        assert data[0]['id'] == group.id.hex
