from Menue import Menue

def main():
    menue = Menue(7, 800, 800)
    menue.turt_init()
    
    menue.onkeypress(menue.follow_path, 'space')
    menue.onkeypress(menue.create_maze, 'Right')
    menue.onkeypress(menue.classic, 'c')
    menue.onkeypress(menue.exit, 'q')
    menue.onscreenclick(menue.get_mouse_click_coor, btn=-1)
    
    menue.listen()
    menue.done()
 

if __name__ == "__main__":
    
    main()
    