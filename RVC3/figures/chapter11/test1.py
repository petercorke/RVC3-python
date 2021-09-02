from machinevisiontoolbox import *


# im = Image.Read('flowers4.png', grey=False) #, dtype='float')

# im2 = Image(np.zeros(im.shape, dtype=np.uint8))
# im2 = im2.paste(128*np.ones((200,200)), (200,150)).colorize()

# im.blend(im2, 0).disp()
# im.blend(im2, 1).disp()
# im.blend(im2, 0.5).disp()

# plt.show(block=True)

# im1 = Image.Read('flowers3.png', grey=False) #, dtype='float')
# im2 = Image.Read('flowers4.png', grey=False) #, dtype='float')

# m = Image(np.zeros(im1.shape[:2], dtype=np.uint8))
# m = m.paste(np.ones((200,200)), (200,150))
# m.disp(title='mask top')
# # im1.switch(m, im2).disp()
# im1.switch(m, [200,0,0]).disp('done')
# plt.show(block=True)


im1 = Image.Read('flowers3.png', grey=True, dtype='float')
im1.disp('original')
im1 = im1.colorize()
idisp(im1.image, block=True)
# im1.disp(block=True)