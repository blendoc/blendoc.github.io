import bpy
import math
import sys
#sys.path.append("C:\Tools\Blender\Blender-build\build_windows_x64_vc16_Release\bin\Release\2.92\python\lib\site-packages")

import numpy as np
import aud

def calculate_db(sound):
    db = dict()
    max = sound.data().max() * strip.volume
    min = sound.data().min() * strip.volume

    if abs(max) > abs(min):
        peak = abs(max)
    else:
        peak = abs(min)

    db["SPF"] = 20 * math.log10(peak)
    
    samples = sound.data()
    m = np.mean(samples**2)
    rms =  np.sqrt(m)
    db["RMS"] = 20 * math.log10(rms)
    print("Decibel value", db)    
    
    return db

def convert_frame_to_time(frame):
    time = dict()
    time["from"] = (frame - strip.frame_final_start) / fps
    time["to"] = (frame - strip.frame_final_start + 1 ) / fps
    #print("Time from", time["from"],"Time to:", time["to"])
    return time

strip = bpy.context.scene.sequence_editor.active_strip
depsgraph = bpy.context.evaluated_depsgraph_get()
sound = strip.sound.evaluated_get(depsgraph).factory

sample_rate = sound.specs[0]

nr_of_samples = sound.length
duration = nr_of_samples/sample_rate


nr_of_frames = strip.frame_final_end - strip.frame_final_start
nr_of_samples_per_frame = nr_of_samples/nr_of_frames

cur_frame = bpy.context.scene.frame_current
fps = bpy.context.scene.render.fps / bpy.context.scene.render.fps_base
'''
time_from = (cur_frame - 1 - strip.frame_start) / fps
time_to = (cur_frame - strip.frame_start) / fps
sound_cur_frame = sound.limit(time_from, time_to)
calculate_db(sound_cur_frame)
'''

f_old = bpy.context.scene.frame_current
f = strip.frame_final_start
t = convert_frame_to_time(f)
print("final start", strip.frame_final_start, "final end", strip.frame_final_end)
chunk = sound.limit(t["from"],t["to"]).data()
animated_samples = chunk
print("time:", t["from"], "-", t["to"],"size:", len(chunk))
x = 0
while f < strip.frame_final_end:
    #bpy.context.scene.frame_set(f)
    x+= 1
    t = convert_frame_to_time(f)
    chunk = sound.limit(t["from"],t["to"]).data()
    
    animated_samples = np.append(animated_samples, chunk, axis=0)
    print("nr", x,"time:", t["from"], "-", t["to"],"size:", len(chunk), "cum", len(animated_samples))
    f += 1

bpy.context.scene.frame_set(f_old)
print("--------------------")
print("size cum chunks", len(animated_samples))
print("original size", len(sound.data()))





