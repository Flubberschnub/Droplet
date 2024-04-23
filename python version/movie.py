import animation_file
import animator
import writer
import preferences

objects = preferences.presetObjects

def createMovie(objects, lengthInSeconds = 10, timeSpeedFactor = 100, fps = 24, saveCSV = False, csvFileName = 'csvFile', inputFileName = 'testName', fromCSV = False, showPlot = False, fixedFrame = True, final = False, fileType = '.mp4', fileName = 'movieDefault'):

    '''
    objects = preferences.presetObjects, lengthInSeconds = 10, timeSpeedFactor = 100, fps = 24,
    saveCSV = False, csvFileName = 'csvFile',
    inputFileName = 'testName', fromCSV = False,
    showPlot = False,
    fixedFrame = True,
    final = False,
    fileType = '.mp4', fileName = 'movieDefault'
    '''

    animationData = animation_file.createAnimationData(objects, lengthInSeconds, timeSpeedFactor, fps, saveCSV, csvFileName)
    animation = animator.animationCreator(animationData, inputFileName, fromCSV, showPlot, fixedFrame, final)
    writer.writer(animation, fileType, final, fileName)

createMovie(objects, fps = 60, final = True, fileName = '60fpsMovie')
