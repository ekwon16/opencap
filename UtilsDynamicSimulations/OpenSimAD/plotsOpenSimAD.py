import numpy as np

from utilsOpenSimAD import plotVSBounds
from utilsOpenSimAD import plotVSvaryingBounds

def plotGuessVSBounds(lw, uw, w0, trial, nJoints, N, d, guessQsEnd, 
                      guessQdsEnd, withArms=True, 
                      withLumbarCoordinateActuators=True):
    # States.
    # Muscle activation at mesh points.
    
    lwp = lw['A'][trial].to_numpy().T
    uwp = uw['A'][trial].to_numpy().T
    y = w0['A'][trial].to_numpy().T
    title='Muscle activation at mesh points'            
    plotVSBounds(y,lwp,uwp,title)  
    # Muscle activation at collocation points.
    lwp = lw['A'][trial].to_numpy().T
    uwp = uw['A'][trial].to_numpy().T
    y = w0['Aj'][trial].to_numpy().T
    title='Muscle activation at collocation points' 
    plotVSBounds(y,lwp,uwp,title)  
    # Muscle force at mesh points.
    lwp = lw['F'][trial].to_numpy().T
    uwp = uw['F'][trial].to_numpy().T
    y = w0['F'][trial].to_numpy().T
    title='Muscle force at mesh points' 
    plotVSBounds(y,lwp,uwp,title)  
    # Muscle force at collocation points.
    lwp = lw['F'][trial].to_numpy().T
    uwp = uw['F'][trial].to_numpy().T
    y = w0['Fj'][trial].to_numpy().T
    title='Muscle force at collocation points' 
    plotVSBounds(y,lwp,uwp,title)
    # Joint position at mesh points.
    lwp = np.reshape(
        lw['Qsk'][trial], (nJoints, N[trial]+1), order='F')
    uwp = np.reshape(
        uw['Qsk'][trial], (nJoints, N[trial]+1), order='F')
    y = guessQsEnd
    title='Joint position at mesh points' 
    plotVSvaryingBounds(y,lwp,uwp,title)             
    # Joint position at collocation points.
    lwp = np.reshape(
        lw['Qsj'][trial], (nJoints, d*N[trial]), order='F')
    uwp = np.reshape(
        uw['Qsj'][trial], (nJoints, d*N[trial]), order='F')
    y = w0['Qsj'][trial].to_numpy().T
    title='Joint position at collocation points' 
    plotVSvaryingBounds(y,lwp,uwp,title) 
    # Joint velocity at mesh points.
    lwp = lw['Qds'][trial].to_numpy().T
    uwp = uw['Qds'][trial].to_numpy().T
    y = guessQdsEnd
    title='Joint velocity at mesh points' 
    plotVSBounds(y,lwp,uwp,title) 
    # Joint velocity at collocation points.
    lwp = lw['Qds'][trial].to_numpy().T
    uwp = uw['Qds'][trial].to_numpy().T
    y = w0['Qdsj'][trial].to_numpy().T
    title='Joint velocity at collocation points' 
    plotVSBounds(y,lwp,uwp,title) 
    if withArms:
        # Arm activation at mesh points.
        lwp = lw['ArmA'][trial].to_numpy().T
        uwp = uw['ArmA'][trial].to_numpy().T
        y = w0['ArmA'][trial].to_numpy().T
        title='Arm activation at mesh points' 
        plotVSBounds(y,lwp,uwp,title) 
        # Arm activation at collocation points.
        lwp = lw['ArmA'][trial].to_numpy().T
        uwp = uw['ArmA'][trial].to_numpy().T
        y = w0['ArmAj'][trial].to_numpy().T
        title='Arm activation at collocation points' 
        plotVSBounds(y,lwp,uwp,title)
    if withLumbarCoordinateActuators:
        # Lumbar activation at mesh points.
        lwp = lw['LumbarA'][trial].to_numpy().T
        uwp = uw['LumbarA'][trial].to_numpy().T
        y = w0['LumbarA'][trial].to_numpy().T
        title='Lumbar activation at mesh points' 
        plotVSBounds(y,lwp,uwp,title) 
        # Lumbar activation at collocation points.
        lwp = lw['LumbarA'][trial].to_numpy().T
        uwp = uw['LumbarA'][trial].to_numpy().T
        y = w0['LumbarAj'][trial].to_numpy().T
        title='Lumbar activation at collocation points' 
        plotVSBounds(y,lwp,uwp,title)
    # Controls.
    # Muscle activation derivative at mesh points.
    lwp = lw['ADt'][trial].to_numpy().T
    uwp = uw['ADt'][trial].to_numpy().T
    y = w0['ADt'][trial].to_numpy().T
    title='Muscle activation derivative at mesh points' 
    plotVSBounds(y,lwp,uwp,title) 
    if withArms:
        # Arm excitation at mesh points.
        lwp = lw['ArmE'][trial].to_numpy().T
        uwp = uw['ArmE'][trial].to_numpy().T
        y = w0['ArmE'][trial].to_numpy().T
        title='Arm excitation at mesh points' 
        plotVSBounds(y,lwp,uwp,title)
    if withLumbarCoordinateActuators:
        # Lumbar excitation at mesh points.
        lwp = lw['LumbarE'][trial].to_numpy().T
        uwp = uw['LumbarE'][trial].to_numpy().T
        y = w0['LumbarE'][trial].to_numpy().T
        title='Lumbar excitation at mesh points' 
        plotVSBounds(y,lwp,uwp,title)                    
    # Muscle force derivative at mesh points.
    lwp = lw['FDt'][trial].to_numpy().T
    uwp = uw['FDt'][trial].to_numpy().T
    y = w0['FDt'][trial].to_numpy().T
    title='Muscle force derivative at mesh points' 
    plotVSBounds(y,lwp,uwp,title)
    # Joint velocity derivative (acceleration) at mesh points.
    lwp = lw['Qdds'][trial].to_numpy().T
    uwp = uw['Qdds'][trial].to_numpy().T
    y = w0['Qdds'][trial].to_numpy().T
    title='Joint velocity derivative (acceleration) at mesh points' 
    plotVSBounds(y,lwp,uwp,title)
    