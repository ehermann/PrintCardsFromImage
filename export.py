
from PIL import Image
import numpy as np


def save_page(img,orig_layout,layout,page=0,verso=False,prefix="page"):

    im = Image.open(img)
    card=np.array([im.size[0],im.size[1]])//orig_layout
    p_layout=dst_layout*card
    if page*layout[0]*layout[1]>=orig_layout[0]*orig_layout[1]:
        return False
        ##approximate A4
    if(p_layout[1]/p_layout[0]>1.414):
        p_layout[0]=int(p_layout[1]*1/1.414)
    else:
        p_layout[1]=int(p_layout[0]*1.414)
  
    direction=1
    edge=0
    if verso:
        direction=-1
        edge= p_layout[0]-card[0]
    im_new = Image.new(mode = "RGB", size = (p_layout[0],p_layout[1]),color=(255,255,255,0) )
    r=min(layout[0]*layout[1],orig_layout[0]*orig_layout[1]-page*layout[0]*layout[1])
    for x in range (r):
        x_orig=page*layout[0]*layout[1]+x
        src_0=np.array([x_orig%orig_layout[0],x_orig//orig_layout[0]])*card
        dst_0=np.array([x%layout[0],x//layout[0]])
        dst_0[0]= edge+direction*dst_0[0]*card[0]
        dst_0[1]=dst_0[1]*card[1]
        src_n=src_0+card
        
        region = im.crop((src_0[0], src_0[1], src_n[0], src_n[1]))
        im_new.paste(region,(dst_0[0], dst_0[1]))
        
    #im_new.show()
    im_new.save(prefix+str(page)+".pdf")
    return True

orig_layout=np.array ([10,7])



dst_layout=np.array([4,3])

p=0
while save_page("verso.jpg",orig_layout,dst_layout,page=p,prefix="verso",verso=True):
        p=p+1
