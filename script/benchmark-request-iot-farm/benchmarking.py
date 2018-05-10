#! /usr/bin/python
import ck.kernel as ck
import copy
import re
import argparse


# ReQuEST description.
request_dict={
  'report_uid':'640fb4c4b9ba9822', # unique UID for a given ReQuEST submission generated manually by user (ck uid)
                                   # the same UID will be for the "report" and "artifact" (in the same repo)

  'repo_uoa':'ck-request-asplos18-iot-farm',
  'repo_uid':'9bb172637b2083c2',

  'repo_cmd':'ck pull repo:ck-request-asplos18-iot-farm',

  'farm':'', # if farm of machines

  'algorithm_species':'4b8bbc192ec57f63' # image classification
}

# Platform tags.
platform_tags=''

program='request-iot-benchmark'

# Number of statistical repetitions.
num_repetitions=3 # however there is already an internal stat. repetition ...

def do(i, arg):

    random_name = arg.random_name

    target=arg.target

    cmd_key=arg.cmd_key

    # Detect basic platform info.
    ii={'action':'detect',
        'module_uoa':'platform',
        'target':target,
        'out':'out'}
    r=ck.access(ii)
    if r['return']>0: return r

    # Keep to prepare ReQuEST meta.
    platform_dict=copy.deepcopy(r)

    # Host and target OS params.
    hos=r['host_os_uoa']
    hosd=r['host_os_dict']

    tos=r['os_uoa']
    tosd=r['os_dict']
    tdid=r['device_id']

    ii={'action':'pipeline',
        'prepare':'yes',

        'module_uoa':'program',
        'data_uoa':program,
        'cmd_key':cmd_key,

        'target':target,
        'target_os':tos,
        'device_id':tdid,

        'no_state_check':'yes',
        'no_compiler_description':'yes',
        'skip_calibration':'yes',

       'cpu_freq':'max',
       'gpu_freq':'max',

        'flags':'-O3',
        'speed':'no',
        'energy':'no',

        'skip_print_timers':'yes',
        'out':'con'
    }

    r=ck.access(ii)
    if r['return']>0: return r

    fail=r.get('fail','')
    if fail=='yes':
        return {'return':10, 'error':'pipeline failed ('+r.get('fail_reason','')+')'}

    ready=r.get('ready','')
    if ready!='yes':
        return {'return':11, 'error':'pipeline not ready'}

    state=r['state']
    tmp_dir=state['tmp_dir']

    # Remember resolved deps for this benchmarking session.
    xdeps=r.get('dependencies',{})

    # Clean pipeline.
    if 'ready' in r: del(r['ready'])
    if 'fail' in r: del(r['fail'])
    if 'return' in r: del(r['return'])

    pipeline=copy.deepcopy(r)

    for dummy in ['dummy']:
        for dummy2 in ['dummy2']:
            record_repo='local'
            record_uoa='ck-request-asplos18-iot-farm-'+cmd_key

            # Prepare pipeline.
            ck.out('---------------------------------------------------------------------------------------')
            ck.out('CMD key - '+cmd_key)
            ck.out('Experiment - %s:%s' % (record_repo, record_uoa))

            # Prepare autotuning input.
            cpipeline=copy.deepcopy(pipeline)

            cpipeline['cmd_key']=cmd_key

            # Prepare common meta for ReQuEST tournament
            features=copy.deepcopy(cpipeline['features'])
            platform_dict['features'].update(features)

            r=ck.access({'action':'prepare_common_meta',
                         'module_uoa':'request.asplos18',
                         'platform_dict':platform_dict,
                         'deps':cpipeline['dependencies'],
                         'request_dict':request_dict})
            if r['return']>0: return r

            record_dict=r['record_dict']

            meta=r['meta']

            if random_name:
               rx=ck.gen_uid({})
               if rx['return']>0: return rx
               record_uoa=rx['data_uid']

            tags=r['tags']

            tags.append(program)

            ii={'action':'autotune',

                'target':target,

                'module_uoa':'pipeline',
                'data_uoa':'program',

                'iterations':1,
                'repetitions':num_repetitions,

                'record':'yes',
                'record_failed':'yes',
                'record_params':{
                    'search_point_by_features':'yes'
                },

                'tags':tags,
                'meta':meta,

                'record_dict':record_dict,

                'record_repo':record_repo,
                'record_uoa':record_uoa,

                'pipeline':cpipeline,
                'out':'con'}

            r=ck.access(ii)
            if r['return']>0: return r

            fail=r.get('fail','')
            if fail=='yes':
                return {'return':10, 'error':'pipeline failed ('+r.get('fail_reason','')+')'}

            skip_compile='yes'

    return {'return':0}

##############################################################################################

parser = argparse.ArgumentParser(description='Pipeline')
parser.add_argument("--target", action="store", default='', dest="target")
parser.add_argument("--cmd_key", action="store", default='benchmark-alexnet-single-device-cpu', dest="cmd_key")
parser.add_argument("--target_os", action="store", dest="tos")
parser.add_argument("--device_id", action="store", dest="did")
parser.add_argument("--random_name", action="store_true", default=False, dest="random_name")
myarg=parser.parse_args()

r=do({}, myarg)
if r['return']>0: ck.err(r)
