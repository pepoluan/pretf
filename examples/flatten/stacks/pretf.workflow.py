from pretf import workflow


def pretf_workflow():

    with workflow.mirror_files("*.*"):

        return workflow.up()
