

#for i in range(o,len(xloc1)):
    line_segments = LineCollection([zip(xloc1,yloc1) for y in yloc1], # Make a sequence of x,y pairs
                                linewidths    = 1,
                                linestyles = 'solid',
                                cmap=plt.get_cmap(cm))
    plt.add_collection(lcollect)
