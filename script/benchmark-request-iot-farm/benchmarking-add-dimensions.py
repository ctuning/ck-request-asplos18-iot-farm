#! /usr/bin/python
import ck.kernel as ck
import os

# undefined since can't measure for this artifact (simulation)
accuracy_top1=0.0
accuracy_top5=0.0

def do(i):

    # List performance entries
    r=ck.access({'action':'search',
                 'module_uoa':'experiment',
                 'data_uoa':'ck-request-asplos18-iot-farm-benchmark-*'
#                 'repo_uoa':'ck-request-asplos18-results-iot-farm'
                })
    if r['return']>0: return r
    lst=r['lst']

    for q in lst:
        duid=q['data_uid']
        duoa=q['data_uoa']
        ruid=q['repo_uid']
        path=q['path']

        ck.out(duoa)

        # Search matching accuracy entry
        r=ck.access({'action':'load',
                     'module_uoa':'experiment',
                     'data_uoa':duid,
                     'repo_uoa':ruid})
        if r['return']>0: return r

        dd=r['dict']

        ruid=r['repo_uid']
        apath=r['path']             

        # Updating meta if needed
        dd['meta']['scenario_module_uoa']='a555738be4b65860' # module:request.asplos18

        farm=''
        j=duoa.find('-farm-')
        if j>=0:
           j1=duoa.find('-farm-', j+1)
           if j1>=0:
              j2=duoa.find('-nodes', j1+1)
              if j2>=0:
                 farm=duoa[j1+6:j2]

        if farm!='':
           dd['meta']['farm']='RPi farm: '+farm+' devices (Avro)'

           dd['meta']["cpu_name"]="BCM2709"
           dd['meta']["os_name"]="Ubuntu 16.04.2 LTS"
           dd['meta']["plat_name"]="Raspberry Pi (Raspberry Pi 3 Model B)"

        # This is not real image classification, so changing to "image classification simulation"
        dd["meta"]["algorithm_species"]="f4f75a0a6b65e4cd"

        if 'dataset_species' in dd['meta']:
           del(dd['meta']['dataset_species']) # dataset species (non since simulation here)

        dd['meta']['platform_species']='embedded' # embedded vs server vs fpga (maybe other classifications such as edge)

        dd['meta']['artifact']='640fb4c4b9ba9822' # artifact description (ck ls ck-request-asplos18-iot-farm:artifact:*)

        gfreq=''
        cfreq=''

        if farm!='':
           ifarm=int(farm)
           cfreq=1200 #MHz
           dd['meta']['platform_peak_power']=5*ifarm #Watts 
           dd['meta']['platform_price']=40*ifarm # $
           dd['meta']['platform_price_date']='20170811' # when we bought ours
        elif '-rpi' in duoa:
           cfreq=1200 #MHz
           dd['meta']['platform_peak_power']=5 #Watts 
           dd['meta']['platform_price']=40 # $
           dd['meta']['platform_price_date']='20170811' # when we bought ours
        elif '-tx1' in duoa:
           if '-cpu' in duoa:
              cfreq=1734 #MHz
           else:
              gfreq=998 #MHz

           dd['meta']['plat_name']='NVIDIA Jetson TX1'
           dd['meta']['platform_peak_power']=15 #Watts https://devtalk.nvidia.com/default/topic/916735/jetson-tx1/jetson-tx1-power-requirements-and-power-management/
           dd['meta']['platform_price']=435 # $, https://developer.nvidia.com/embedded/buy/jetson-tx1
           dd['meta']['platform_price_date']='20180520' # date
        elif '-tx2' in duoa:
           if '-cpu' in duoa:
              cfreq=2035 #MHz
           else:
              gfreq=1122 #MHz

           dd['meta']['plat_name']='NVIDIA Jetson TX2'
           dd['meta']['platform_peak_power']=15 #Watts https://devblogs.nvidia.com/jetson-tx2-delivers-twice-intelligence-edge/
           dd['meta']['platform_price']=499 # $, https://developer.nvidia.com/embedded/buy/jetson-tx2
           dd['meta']['platform_price_date']='20180520' # date
        else:
           return {'return':1, 'error':'platform is not recognized ('+duoa+')'}

        if 'platform_name' in dd['meta']:
           del(dd['meta']['platform_name'])

        dd['meta']['processed']='yes'

        # Unified full name for some deps
        ds=dd['meta']['deps_summary']

        if ds.get('lib-tensorflow',{}).get('version','')=='':
           ds['lib-tensorflow']['version']='1.5' # we used everywhere TF v1.5

        # for simplicity add manually (can later automate it as in other artifacts, but just didn't have time here)
        if '-alexnet-' in duoa:
           dd['meta']['model_species']='c0ad9b9800422f98' # model.species:alexnet
           dd['meta']["model_design_name"]="AlexNet (authors' implementation)"
           dd['meta']["model_precision"]="fp32"
        elif '-vgg16-' in duoa:
           dd['meta']['model_species']='a3fcac86d42bdbc4' # model.species:vgg16
           dd['meta']["model_design_name"]="VGG 16 (authors' implementation)"
           dd['meta']["model_precision"]="fp32"
        else:
           return {'return':1, 'error':'unknown model ('+duoa+')'}

        if 'model_precision' in dd:
           del(dd['model_precision'])

        x=ds['lib-tensorflow']
        r=ck.access({'action':'make_deps_full_name','module_uoa':'request.asplos18','deps':x})
        if r['return']>0: return r
        dd['meta']['library_name']=r['full_name']

        # Updating entry
        r=ck.access({'action':'update',
                     'module_uoa':'experiment',
                     'data_uoa':duid,
                     'repo_uoa':ruid,
                     'dict':dd,
                     'substitute':'yes',
                     'ignore_update':'yes',
                     'sort_keys':'yes'
                    })
        if r['return']>0: return r

        # Checking points to aggregate
        os.chdir(path)
        dperf=os.listdir(path)
        for f in dperf:
            if f.endswith('.cache.json'):
               os.system('git rm -f '+f)

            elif f.endswith('.flat.json'):
               ck.out(' * '+f)

               # Load performance file 
               p1=os.path.join(path, f)

               r=ck.load_json_file({'json_file':p1})
               if r['return']>0: return r
               d1=r['dict']

               # Prune some old value
               d={}
               for k in d1:
                   if not k.startswith('##characteristics#run#accuracy_top1') and \
                      not k.startswith('##characteristics#run#accuracy_top5') and \
                      not k.startswith('##characteristics#run#inference_throughput') and \
                      not k.startswith('##characteristics#run#inference_latency'):
                      d[k]=d1[k]

               # for simplicity add manually (can later automate it as in other artifacts, but just didn't have time here)
               d['##features#gpu_freq#min']=gfreq
               d['##features#cpu_freq#min']=cfreq

               freq=gfreq
               if cfreq!='': freq=cfreq
               d['##features#freq#min']=freq

               d['##features#processed#min']='yes'

               # Add throughput (images/second)
               tall=d.get('##characteristics#run#execution_time_classify#all',[]) # It's internal VTA measurements
               if len(tall)>0:
                  tnew=[]
                  for t in tall:
                      t1=1/t
                      tnew.append(t1)
                  
                  r=ck.access({'action':'stat_analysis',
                               'module_uoa':'experiment',
                               'dict':d,
                               'dict1':{'##characteristics#run#inference_throughput':tnew}
                              })
                  if r['return']>0: return r

               # Unify batch size
               batch=1 # for now only 1 is supported in this artifact
               d['##features#batch_size#min']=batch

               # inference latency
               d['##features#measuring_latency#min']='yes'

               r=ck.access({'action':'stat_analysis',
                            'module_uoa':'experiment',
                            'dict':d,
                            'dict1':{'##characteristics#run#inference_latency':tall}
                           })
               if r['return']>0: return r

               r=ck.access({'action':'stat_analysis',
                            'module_uoa':'experiment',
                            'dict':d,
                            'dict1':{'##characteristics#run#prediction_time_avg_s':tall}
                           })
               if r['return']>0: return r

               # Add accuracy (was calculated through separate experiment)
               r=ck.access({'action':'stat_analysis',
                            'module_uoa':'experiment',
                            'dict':d,
                            'dict1':{'##characteristics#run#accuracy_top1':[accuracy_top1]}
                           })
               if r['return']>0: return r

               # Add accuracy (was calculated through separate experiment)
               r=ck.access({'action':'stat_analysis',
                            'module_uoa':'experiment',
                            'dict':d,
                            'dict1':{'##characteristics#run#accuracy_top5':[accuracy_top5]}
                           })
               if r['return']>0: return r

               # Save updated dict
               r=ck.save_json_to_file({'json_file':p1, 'dict':d, 'sort_keys':'yes'})
               if r['return']>0: return r

    return {'return':0}

r=do({})
if r['return']>0: ck.err(r)
