image bg garden = Transform("images/bg_garden.png", xysize=(1920,1080))
image bg corridor = Transform("images/bg_corridor.png", xysize=(1920,1080))
image cg sisters = Transform("images/cg_sisters.png", xysize=(1920,1080))
image miran neutral = Transform("images/miran_neutral.png", ysize=1400, fit="contain")
image miran playful = Transform("images/miran_playful.png", ysize=1400, fit="contain")
image miran hopeful = Transform("images/miran_hopeful.png", ysize=1400, fit="contain")
image miran startled = Transform("images/miran_startled.png", ysize=1400, fit="contain")
image seran neutral = Transform("images/seran_neutral.png", ysize=1425, fit="contain")
image seran playful = Transform("images/seran_playful.png", ysize=1425, fit="contain")
image seran unsettled = Transform("images/seran_unsettled.png", ysize=1425, fit="contain")
image oknyeo neutral = Transform("images/oknyeo_neutral.png", ysize=1350, fit="contain")
image oknyeo wry = Transform("images/oknyeo_wry.png", ysize=1350, fit="contain")
# A small abstract silhouette, intentionally unobtrusive on the white path.
image snake = Text("∿∿", font="DejaVuSans.ttf", size=70, color="#394237")
transform miran_left:
    xcenter 510
    ypos 55
transform seran_right:
    xcenter 1400
    ypos 40
transform seran_middle:
    xcenter 960
    ypos 40
transform oknyeo_right:
    xcenter 1500
    ypos 90
transform bush_close:
    zoom 1.28
    xalign 0.0
    yalign 0.55
transform snake_cross:
    xpos 900
    ypos 630
    alpha 0.0
    linear 0.2 alpha 0.75
    linear 1.3 xpos 1390 ypos 580
    linear 0.3 alpha 0.0
