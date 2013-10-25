from datetime import datetime
from flask import current_app

from changes.config import db, queue
from changes.backends.jenkins.builder import JenkinsBuilder
from changes.constants import Status
from changes.models.build import Build


def sync_build(build_id):
    try:
        build = Build.query.get(build_id)
        if not build:
            return

        if build.status == Status.finished:
            return

        builder = JenkinsBuilder(
            app=current_app,
            base_url=current_app.config['JENKINS_URL'],
        )
        builder.sync_build(build)

        build.date_modified = datetime.utcnow()
        db.session.add(build)

        if build.status != Status.finished:
            queue.delay('sync_build', build_id=build.id.hex)
    except Exception:
        # Ensure we continue to synchronize this build as this could be a
        # temporary failure
        queue.retry('sync_build', build_id=build.id.hex)
        raise
