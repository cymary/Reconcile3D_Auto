def Reconcile3DAuto():
    import nuke
    import nukescripts

    reNode = nuke.thisNode()

    # get the number of inputs connected on the switcher node

    tInputs = nuke.thisNode().input(2).inputs()
    reNodeName = nuke.thisNode().name()
    # get the frame range information

    p = nukescripts.panels.PythonPanel("Reconcile 3D Auto-> R3A")
    k = nuke.String_Knob("framerange","FrameRange") # "framerange" is variable "Frame Range" is label
    k.setFlag(nuke.STARTLINE)
    p.addKnob(k)
    k.setValue("%s-%s" % (nuke.root().firstFrame(), nuke.root().lastFrame()))
    result = p.showModalDialog()
    if result == 0:
       return None
    try:
        fRange = nuke.FrameRange(p.knobs()["framerange"].getText())
    except:
        if nuke.GUI:
            nuke.message( 'Framerange format is not correct, use startframe-endframe i.e.: 0-200' )

    # add the tracks in the tracking node

    Stracker = nuke.createNode('Tracker4')

    tarTrack = Stracker['tracks']
    numColumns = 31
    colTrackX = 2
    colTrackY = 3


    firstFrame = str(fRange).split('-')[0]
    lastFrame = str(fRange).split('-')[1]



    for item in range(0,tInputs):
        print item


        nuke.toNode(reNodeName).knob('which').setValue(item)

        nuke.execute("%s"%reNode.knob('name').getValue(),int(firstFrame),int(lastFrame))
        print ">>>>>>>>>>>>>>%s"%item

        eachTrack = Stracker['add_track'].execute()

        for cFrame in fRange:
            #get the x and y for this frame

            reNodeXpos = reNode['output'].getValueAt(cFrame)[0]
            reNodeYpos = reNode['output'].getValueAt(cFrame)[1]

            x = float(reNodeXpos)
            y = float(reNodeYpos)

            #set the x and y for this track on this frame
            tarTrack.setValueAt(x, cFrame, numColumns*(item) + colTrackX)
            tarTrack.setValueAt(y, cFrame, numColumns*(item) + colTrackY)

    Stracker['add_track'].execute()
    Stracker['del_tracks'].execute()


    return None
