import play

vloer = play.new_box(y=-200, width=600, height=20)

for i in range(10):
    bal = play.new_circle(y=200, x=-225+45*i, radius=20)
    bal.start_physics(bounciness=i*0.1)