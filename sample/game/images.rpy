image bg garden = Transform("images/bg_garden.png", xysize=(1920,1080))
image bg corridor = Transform("images/bg_corridor.png", xysize=(1920,1080))
image cg sisters = Transform("images/cg_sisters.png", xysize=(1920,1080))
image bg hall = Transform("images/bg_hall.png", xysize=(1920,1080))
image bg street = Transform("images/bg_street.png", xysize=(1920,1080), matrixcolor=BrightnessMatrix(-0.12))
image bg street_rain = Transform("images/bg_street.png", xysize=(1920,1080), matrixcolor=BrightnessMatrix(-0.35)*SaturationMatrix(0.65))
image bg restaurant = Transform("images/bg_restaurant.png", xysize=(1920,1080))
image bg restaurant_dark = Transform("images/bg_restaurant.png", xysize=(1920,1080), matrixcolor=BrightnessMatrix(-0.16))
image bg apartment = Transform("images/bg_apartment.png", xysize=(1920,1080))
image bg apartment_dark = Transform("images/bg_apartment.png", xysize=(1920,1080), matrixcolor=BrightnessMatrix(-0.38))
image bg apartment_candle = Transform("images/bg_apartment_candle.png", xysize=(1920,1080))
image bg apartment_dawn = Transform("images/bg_apartment_dawn.png", xysize=(1920,1080))
image bg garden_evening = Transform("images/bg_garden.png", xysize=(1920,1080), matrixcolor=BrightnessMatrix(-0.12))
image bg cinema = Transform("images/bg_cinema.png", xysize=(1920,1080))
image cg candle = Transform("images/cg_candle.png", xysize=(1920,1080))
image danju neutral = Transform("images/danju_neutral.png", ysize=1250, fit="contain")
image hyunma neutral = Transform("images/hyunma_neutral.png", ysize=1650, fit="contain")
image miran neutral = Transform("images/miran_neutral.png", ysize=1050, fit="contain")
image miran playful = Transform("images/miran_playful.png", ysize=1050, fit="contain")
image miran hopeful = Transform("images/miran_hopeful.png", ysize=1050, fit="contain")
image miran startled = Transform("images/miran_startled.png", ysize=1050, fit="contain")
image miran coat = Transform("images/miran_coat.png", ysize=1050, fit="contain")
image seran neutral = Transform("images/seran_neutral.png", ysize=1075, fit="contain")
image seran playful = Transform("images/seran_playful.png", ysize=1075, fit="contain")
image seran unsettled = Transform("images/seran_unsettled.png", ysize=1075, fit="contain")
image oknyeo neutral = Transform("images/oknyeo_neutral.png", ysize=1015, fit="contain")
image oknyeo wry = Transform("images/oknyeo_wry.png", ysize=1015, fit="contain")
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
transform man_left:
    xcenter 450
    ypos 15
transform man_middle:
    xcenter 960
    ypos 15
transform man_right:
    xcenter 1450
    ypos 15
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
