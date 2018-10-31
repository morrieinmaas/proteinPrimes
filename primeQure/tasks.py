from __future__ import absolute_import
import time
import json
import logging
from sympy.ntheory import factorint
from proteinPrimes.celery import app
from .models import Job
from channels import Channel

log = logging.getLogger(__name__)

@app.task
def sec3(job_id, reply_channel):
    log.info("job_id=%s", job_id)
    # Change task status to completed
    job = Job.objects.all().get(pk=job_id)
    log.debug("Running job_name=%s", job.name)
    job.result_dict = factorint(int(job.name))
    # The following conveniently converts our dict object of the
    # result into the desired string. This is much handier/neater
    # than custom filter or template magic in this case
    job.result_str = "The result is " + " and ".join("{}^({})".format(key, value) for key, value in job.result_dict.items()) 
    log.info(job.result_str)
    job.status = "completed"
    # Add a timeout to force different status in UI
    # Otherwise it instantly show complete because the 
    # factorization performs too quickly
    time.sleep(3)
    job.save()

    # Send status update back to browser client
    if reply_channel is not None:
        Channel(reply_channel).send({
            "text": json.dumps ({
                "action": "completed",
                "job_id": job.id,
                "job_name": job.name,
                "job_status": job.status,
                "job_result": job.result_str,
            })
        })

