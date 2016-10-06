def write_ppm(ppmfilename, width, height, heatmap):
    ppmfile = open(ppmfilename, 'w')
    ppmfile.write('P2\n') 
    ppmfile.write('%s %s\n' % (width, height))
    # Write the color depth
    ppmfile.write('256\n')
    for heat in heatmap:
        if heat > 255:
            ppmfile.write('%s\n' % 255)
        else:
            ppmfile.write('%s\n' % heat)
    ppmfile.close()


def write_heatmap(ppmfilename, binary=False):
    pointers = [int(p.split(',')[0]) for p in open('pointers.txt').readlines()]
    sizes = [int(p.split(',')[1]) for p in open('pointers.txt').readlines()]
    # We get some 64 bit pointers, hack this to display in a 512 x 512.
    pointers = [p & 0xffffffff for p in pointers]
    minp = min(pointers)
    maxp = max(pointers)
    pointers = [p-minp for p in pointers]

    width = 512
    height = 512
    size = width * height
    heatmap = [0] * width * height

    if maxp - minp < width * height * 512:
        pagesize = 512
    elif maxp - minp < width * height * 1024:
        pagesize = 1024
    elif maxp - minp < width * height * 2048:
        pagesize = 2048
    elif maxp - minp < width * height * 4096:
        pagesize = 4096
    else:
        pagesize = 4096

    print 'Page size used: %s' % pagesize

    def page(id):
        p = id / pagesize
        if p >= size:
            return size - 1
        return p

    for p, s in zip(pointers, sizes):
        for pp in xrange(p, p+s):
            heatmap[page(pp)] += 1

    if binary:
        heatmap = [(255 if h > 0 else 0) for h in heatmap]
    else:
        heatmap = [int((h * 1.0 / pagesize) * 255) for h in heatmap]
    write_ppm(ppmfilename, width, height, heatmap)


if __name__ == '__main__':
    write_heatmap('heat.ppm')
    write_heatmap('heatb.ppm', binary=True)
