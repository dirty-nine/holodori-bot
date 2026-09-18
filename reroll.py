import pyautogui
import time
import keyboard
import imageDetect
     
def fill_user_info():
    next_screen_forgiving((1620,61,(255,255,255)), (990,990), (883,433,(40,195,255))) # tap to start > language
    next_screen((883,433,(40,195,255)), (1356,883), (1356,883,(200,200,215))) # language > country
    next_screen((1356,883,(200,200,215)), (615,600), (1356,883,(255,255,255))) # country unchecked > country checkbox
    next_screen((1356,883,(255,255,255)), (1356,883), (1356,883,(200,200,215))) # country checked > birthdate
    fill_out_screen((1356,883,(200,200,215)), (685,480), (1356,883,(255,255,255)), "2000", "10") # birthdate unfilled out > birthday filled out
    next_screen((1356,883,(255,255,255)), (1356,883), (435,568,(255,255,255))) # birthdate filled out > account link
    next_screen((435,568,(255,255,255)), (1356,883), (1383,890,(31,153,215))) # account link > register name
    fill_out_screen((1383,890,(31,153,215)), (950,487), (1383,890,(40,195,255)), "ore") # register name unfilled > register name filled
    next_screen((1383,890,(40,195,255)), (1383,890), (1588,973,(40,195,255))) # register name filled > start with changes
    next_screen_forgiving((1588,973,(40,195,255)), (1588,973), (1727,72,(39,195,255))) # start with changes > group select

def holomem_select():
    #holomem select screen
    next_screen_forgiving((1603,83,(101,221,238)), (307,737), (1616,1045,(207,186,184))) # group select > holomem select
    next_screen((1616,1045,(207,186,184)), (1616,1045), (915,961,(184,98,114))) # holomem select > korone info
    next_screen((915,961,(184,98,114)), (1548,974), (1212,991,(255,255,255))) # korone info > korone confirm
    next_screen_forgiving((1212,991,(255,255,255)), (1548,974), (628,295,(45,197,253))) # korone confirm > blue loading screen (end of character creation)

def next_screen(current_pixel: tuple, next_click_coords: tuple, target_pixel: tuple):
    curr_x, curr_y, curr_rgb = current_pixel
    target_x, target_y, target_rgb = target_pixel
    click_x, click_y = next_click_coords
    
    attempt_seconds = 10
    attempt_delay = 0.2
    
    end_time = time.time() + attempt_seconds
    while time.time() < end_time:
        # Check if we are currently on the correct screen
        if pyautogui.pixelMatchesColor(curr_x, curr_y, curr_rgb):
            pyautogui.click(click_x, click_y)
        time.sleep(attempt_delay)
        
        # Check if we successfully reached the target screen
        if pyautogui.pixelMatchesColor(target_x, target_y, target_rgb):
            return True
    
    print(f"Couldn't navigate to the next screen: target pixel mismatch after {attempt_seconds} seconds.")

def next_screen_forgiving(current_pixel: tuple, next_click_coords: tuple, target_pixel: tuple, threshold: int = 10):
    curr_x, curr_y, curr_rgb = current_pixel
    target_x, target_y, target_rgb = target_pixel
    click_x, click_y = next_click_coords
    
    attempt_seconds = 25
    attempt_delay = 0.2
    
    end_time = time.time() + attempt_seconds
    while time.time() < end_time:
        # Check if we are currently on the correct screen
        if pixelMatchesColorWithThreshold(curr_x, curr_y, curr_rgb, threshold):
            pyautogui.click(click_x, click_y)
        time.sleep(attempt_delay)
        
        # Check if we successfully reached the target screen
        if pixelMatchesColorWithThreshold(target_x, target_y, target_rgb, threshold):
                return True
    
    print("Couldn't navigate to the next screen: target pixel mismatch after 20 seconds.")

def fill_out_screen(current_pixel: tuple, next_click_coords: tuple, target_pixel: tuple, to_write_1: str, to_write_2: str = ""):
    curr_x, curr_y, curr_rgb = current_pixel
    target_x, target_y, target_rgb = target_pixel
    click_x, click_y = next_click_coords

    attempt_seconds = 3
    attempt_delay = 0.3
    
    end_time = time.time() + attempt_seconds
    while time.time() < end_time:
        # Check if we are currently on the correct screen
        if pyautogui.pixelMatchesColor(curr_x, curr_y, curr_rgb):
            pyautogui.click(click_x,click_y)
            pyautogui.typewrite(to_write_1)
            if to_write_2:
                pyautogui.typewrite(to_write_2)
            #finished typing birthdate numbers
        time.sleep(attempt_delay)
        
        # Check if we successfully reached the target screen
        if pyautogui.pixelMatchesColor(target_x, target_y, target_rgb):
            return True
                
    raise RuntimeError("Couldn't navigate to the next screen: target pixel mismatch after 3 attempts.")
    
def pixelMatchesColorWithThreshold(x:int, y:int, rgb_val:tuple, threshold:int = 10):
    target = pyautogui.pixel(x, y)
    return (target[0] - threshold <= rgb_val[0] and rgb_val[0] <= target[0] + threshold and
            target[1] - threshold <= rgb_val[1] and rgb_val[1] <= target[1] + threshold and
            target[2] - threshold <= rgb_val[2] and rgb_val[2] <= target[2] + threshold)    

def is_cutscene():
    end_time = time.time() + 5
    while time.time() < end_time:
        print(".", end="")
        # Check if we are currently on the correct screen
        if not pixelMatchesColorWithThreshold(1450, 460, (45, 197, 253)): # if we ARE actually out of the blue loading screen and see the place description...
            pyautogui.click(990,990) #click screen to check if on a loading screen
            pyautogui.sleep(0.4)
            print("\ndouble checked, blue screen here!")
            
            if not (pixelMatchesColorWithThreshold(1818, 81, (255,255,255), 5) and pixelMatchesColorWithThreshold(921, 469, (255,255,255))): # if skip and pause DONT show up, then not in a cutscene, so return
                print("actually, not in a cut scene. exiting process...")
                return False
            # editor note: above code may be redundant... consider deletion
            return True
        
        pyautogui.sleep(0.4)
    print("could not ...")
    return False

def skip_cutscene():
    next_screen_forgiving((1818,81,(255,255,255)), (1818,81), (1595,972,(40,195,255))) # pause icon appear > skip confirm
    
    pyautogui.sleep(0.2)
    
    next_screen_forgiving((1595,972,(40,195,255)), (1595,972), (1450, 460, (45, 197, 253))) # skip confirm > blue loading screen
    
    print("pause and skip confirm clicked!")
    return True
    
def is_ui_tutorial():
    # blue corner checks
    confidence = imageDetect.findIconConfidenceEdge(r"C:\Users\Nathaniel Wan\Desktop\Programs\holodori_reroll\assets\ui-tutorial-fubuki.png")[0] # fubuki quest ui tutorial
    if confidence > 0.8:
        print(f"confident i found a ui tutorial! ({confidence})")
        return True
    
    confidence = imageDetect.findIconConfidenceEdge(r"C:\Users\Nathaniel Wan\Desktop\Programs\holodori_reroll\assets\ui-tutorial-live.png")[0] # fubuki quest ui tutorial
    if confidence > 0.8:
        print(f"confident i found a ui tutorial! ({confidence})")
        return True
    
    confidence = imageDetect.findIconConfidenceEdge(r"C:\Users\Nathaniel Wan\Desktop\Programs\holodori_reroll\assets\ui-tutorial-house.png")[0] # fubuki quest ui tutorial
    if confidence > 0.8:
        print(f"confident i found a ui tutorial! ({confidence})")
        return True
    
    # unsuccessful check
    print(f"couldn't find any type of ui tutorial... ({confidence})")
    return False

def is_interactable():
    image = imageDetect.findIconConfidence(r"C:\Users\Nathaniel Wan\Desktop\Programs\holodori_reroll\assets\e-interact.png")
    isConfident = image[0]
    if isConfident > 0.8:
        return True
    return False    

def teleport_to_objective():
    clicked_objective = False
    clicked_move = False
    
    while True:
        print("clicking objective...")
        keyboard.press_and_release("space")
        pyautogui.sleep(0.5)
        keyboard.press("alt")
        pyautogui.sleep(0.2)
        clicked_objective = click_icon("objective-icon", width = 100, height = 650, max_time=9999, threshold=0.9)
        if clicked_objective:
            pyautogui.sleep(0.3)
            keyboard.release("alt")
            break
        pyautogui.sleep(0.1)
        
    while True:
        print("clicking move...")
        clicked_move = click_icon("move-button", max_time=9999)
        if clicked_move: break
        pyautogui.sleep(0.1)

    return clicked_objective and clicked_move

def is_loading_screen():
    print("finding loading screen...")
    return pixelMatchesColorWithThreshold(973,555,(72,206,251),20) or pixelMatchesColorWithThreshold(628,295,(45,197,253)) or pixelMatchesColorWithThreshold(1748,243,(255,144,161)) or pixelMatchesColorWithThreshold(506,386,(247,199,43)) or pixelMatchesColorWithThreshold(971,550,(99,220,237),15)

def move_to_objective():
    keyboard.press("w")
    attempt_seconds = 10
    end_time = time.time() + attempt_seconds
    while time.time() < end_time:
        if is_interactable() or is_loading_screen():
            keyboard.release("w")
            if is_interactable():
                print("found interactable")
                keyboard.press_and_release("e")
            if is_loading_screen():
                print("found loading screen")
                return True
            pyautogui.sleep(0.1)  
            if keyboard.is_pressed('w'): return False #debug purposes
        pyautogui.sleep(0.1)
    return False
    
def complete_user_info():
    while True:
        fill_user_info()
        break

def complete_holomem_select():
    while True:
        holomem_select()
        break
    
def skip_cutscenes(repetitions:int = 1):
    skipped=False
    for i in range(repetitions):
        end_time = time.time() + 10
        while time.time() < end_time:
            if is_cutscene(): 
                skip_cutscene() 
                skipped=True
            pyautogui.sleep(0.2)
            print(f"skipped cutscene {i}/{repetitions}!")

def skip_ui_tutorial():
    wasUI = False
    while True: # click screen to get out of quest tutorial
        if is_ui_tutorial(): wasUI = True
        pyautogui.click(990,990)
        if not is_ui_tutorial() and wasUI: break
        pyautogui.sleep(0.2)
        
def complete_objective():
    teleported = False
    while True:
        if pyautogui.pixelMatchesColor(1820, 80, (255,255,255)):
            print("teleporting to objective")
            while True:
                if teleport_to_objective(): 
                    teleported = True
                    break
        if not pyautogui.pixelMatchesColor(1820, 80, (255,255,255)) and teleported: break
        pyautogui.sleep(0.1)

    walked = False
    while True:
        if pyautogui.pixelMatchesColor(1820, 80, (255,255,255)):
            pyautogui.sleep(2)
            print("walking to objective")
            while True:
                if move_to_objective(): 
                    walked = True
                    break
        if not pyautogui.pixelMatchesColor(1820, 80, (255,255,255)) and walked: break
        pyautogui.sleep(0.1)


def roll_gacha():
    skipped = False
    skip_coords = imageDetect.findIconConfidenceCenter(r"C:\Users\Nathaniel Wan\Desktop\Programs\holodori_reroll\assets\skip-icon.png")
    print(f"skip coords{skip_coords}")
    
    end_time = time.time() + 20
    while time.time() < end_time:
        if skip_coords[0] < 0.8:
            skip_coords = imageDetect.findIconConfidenceCenter(r"C:\Users\Nathaniel Wan\Desktop\Programs\holodori_reroll\assets\skip-icon.png")
            print(f"skip coords{skip_coords}")
        if skip_coords[0] > 0.7 or skipped:
            pyautogui.click(*skip_coords[1])
            skipped = True
        
        x_coords = imageDetect.findIconConfidenceCenter(r"C:\Users\Nathaniel Wan\Desktop\Programs\holodori_reroll\assets\blue-x.png")
        print(f"blue x coords{x_coords}")
        if skipped and x_coords[0] > 0.8:
            return True
        pyautogui.sleep(0.1)
    print("gacha error timeout...")
    return False

def click_icon(icon_file_name: str, action:str = "LEFT", max_time = 20, width = 0, height = 0, threshold = 0.8):
    if not icon_file_name.__contains__(".png"): icon_file_name += ".png"
    
    confirmed = False
    end_time = time.time() + max_time
    while time.time() < end_time:
        image = imageDetect.findIconConfidenceCenter(rf"C:\Users\Nathaniel Wan\Desktop\Programs\holodori_reroll\assets\{icon_file_name}", width=width, height=height)
        isConfident = image[0] > threshold
        foundCoords = image[1]
        
        if isConfident:
            if action == "LEFT":
                pyautogui.click(*foundCoords)
            else:
                keyboard.press_and_release(action)
            confirmed = True
        pyautogui.sleep(0.3)
    
        if not isConfident and confirmed:
            return True
        pyautogui.sleep(0.1)
    return False


while True:
    print("script start!")

    # 1
    print("\nawaiting filling in user info... (1)")
    complete_user_info()
    print("completed filling in user info!")

    # 2
    print("\ngoing through holomem select... (2)")
    complete_holomem_select()
    print("completed holomem select...")

    
    for i in range(3):
        end_time = time.time() + 10
        while time.time() < end_time:
            pyautogui.click(900,900)
            pyautogui.sleep(1)
            if (pixelMatchesColorWithThreshold(1818, 81, (255,255,255), 5) and pixelMatchesColorWithThreshold(921, 469, (255,255,255))):
                click_icon("skip-icon")
                pyautogui.sleep(1)
                if i != 1:
                    click_icon("ok")
                break
        pyautogui.sleep(4)
        
    
    
    # 4
    pyautogui.sleep(4)
    print("\nskipping ui tutorial (quest)... (4)")
    skip_ui_tutorial()
    print("skipped ui tutorial (quest)!")

    # # 5
    pyautogui.sleep(2)
    print("clicking blue x...")
    click_icon("blue-x")

    # # 6
    pyautogui.sleep(2)
    print("\ncompleting objective...")
    complete_objective()
    for i in range(1):
        end_time = time.time() + 10
        while time.time() < time.time() + end_time:
            pyautogui.click(900,900)
            pyautogui.sleep(1)
            if (pixelMatchesColorWithThreshold(1818, 81, (255,255,255), 5) and pixelMatchesColorWithThreshold(921, 469, (255,255,255))):
                click_icon("skip-icon")
                pyautogui.sleep(1)
                if i != 1:
                    click_icon("ok")
                break
        pyautogui.sleep(4)
    pyautogui.sleep(6)
    for i in range(2):
        complete_objective()
        for i in range(1):
            end_time = time.time() + 10
            while time.time() < time.time() + end_time:
                pyautogui.click(900,900)
                pyautogui.sleep(1)
                if (pixelMatchesColorWithThreshold(1818, 81, (255,255,255), 5) and pixelMatchesColorWithThreshold(921, 469, (255,255,255))):
                    click_icon("skip-icon")
                    pyautogui.sleep(1)
                    if i != 1:
                        click_icon("ok")
                    break
        pyautogui.sleep(4)
    print("\nobjectives competed!")
    complete_objective()

    # 7
    pyautogui.sleep(2)
    print("rolling gacha...")
    roll_gacha()
    print("rolled gacha!")

    # 8
    pyautogui.sleep(2)
    print("clicking blue x...")
    click_icon("blue-x")

    # 9
    pyautogui.sleep(2)
    print("clicking confirm...")
    click_icon("confirm")

    pyautogui.sleep(2)
    print("re-interacting...")
    click_icon("e-interact", "e")
    click_icon("e-interact", "e")

    pyautogui.sleep(2)
    print("challenging")
    click_icon("challenge-song.png")

    pyautogui.sleep(2)
      
    click_icon("blue-x")

    pyautogui.sleep(2)
    print("confirming song...")
    click_icon("confirm-song")

    pyautogui.sleep(2)
    print("confirming speed...")
    click_icon("confirm-speed")


    pyautogui.sleep(2)
    print("checking download additional...")
    click_icon("ok.png", max_time=3)

    pyautogui.sleep(2)
    print("clicking blue x...")
    click_icon("blue-x",max_time=120)

    pyautogui.sleep(2)
    print("clicking next...")
    if click_icon("next-song", max_time=120): print("clicked next!")
    else: print("failed to click next...")

    pyautogui.sleep(4)
    for i in range(1):
        end_time = time.time() + 10
        while time.time() < time.time() + end_time:
            pyautogui.click(900,900)
            pyautogui.sleep(1)
            if (pixelMatchesColorWithThreshold(1818, 81, (255,255,255), 5) and pixelMatchesColorWithThreshold(921, 469, (255,255,255))):
                click_icon("skip-icon")
                pyautogui.sleep(1)
                if i != 1:
                    click_icon("ok")
                break
        pyautogui.sleep(4)

    pyautogui.sleep(2)
    print("skipping ui tutorial (map)....")
    click_icon("ui-tutorial-map")

    pyautogui.sleep(2)
    print("skipping ui tutorial (map quests)....")
    click_icon("ui-tutorial-quests")

    pyautogui.sleep(2)
    print("skipping ui tutorial (map exit)....")
    click_icon("ui-tutorial-map-exit")


    pyautogui.sleep(2)
    for i in range(4):
        teleport_to_objective()
        pyautogui.sleep(0.3)

        move_to_objective()

        pyautogui.sleep(1)
        skip_cutscenes()
        pyautogui.sleep(0.5)

    pyautogui.sleep(2)
    click_icon("tap-to-close-big")
    pyautogui.sleep(2)
    click_icon("tap-to-continue")
    pyautogui.sleep(2)
    click_icon("ok")


    pyautogui.sleep(2)
    click_icon("ui-tutorial-live")


    pyautogui.sleep(2)
    click_icon("ui-tutorial-house")


    pyautogui.sleep(2)
    click_icon("tap-to-close-banner", threshold=0.4)

    pyautogui.sleep(2)
    click_icon("tap-to-close-big", threshold=0.4)

    pyautogui.sleep(2)
    click_icon("tap-to-close-login", threshold=0.4)

    pyautogui.sleep(2)
    click_icon("tap-to-close-big", threshold=0.4)

    pyautogui.sleep(3)
    while click_icon("blue-x-banner", max_time = 2): 
        print("clicked blue x banner!")

    pyautogui.sleep(2)
    keyboard.press_and_release("space")
    pyautogui.sleep(0.5)
    keyboard.press_and_release("space")
    pyautogui.sleep(2)
    keyboard.press("alt")
    pyautogui.sleep(2)
    click_icon("menu")
    pyautogui.sleep(2)
    keyboard.release("alt")

    pyautogui.sleep(2)
    click_icon("gifts")

    pyautogui.sleep(2)
    click_icon("collect-all")

    pyautogui.sleep(2)
    click_icon("tap-to-close-big")

    pyautogui.sleep(2)
    click_icon("blue-x")

    pyautogui.sleep(2)
    click_icon("yellow-x")

    pyautogui.sleep(2)
    keyboard.press_and_release("space")
    pyautogui.sleep(0.5)
    keyboard.press_and_release("space")
    pyautogui.sleep(2)
    keyboard.press("alt")
    pyautogui.sleep(2)
    click_icon("gacha")
    pyautogui.sleep(2)
    keyboard.release("alt")

    pyautogui.sleep(2)
    while imageDetect.findIconConfidenceCenter(r"C:\Users\Nathaniel Wan\Desktop\Programs\holodori_reroll\assets\gacha-check.PNG")[0] < 0.8:
        banner_path = r"C:\Users\Nathaniel Wan\Desktop\Programs\holodori_reroll\assets\secret-vacation-getaway-gacha-banner.PNG"
        result = imageDetect.findIconConfidenceCenter(banner_path)
        if result[0] > 0.9:
            pyautogui.sleep(2)
            pyautogui.click(*result[1])

    pyautogui.sleep(2)
    click_icon("gacha-check",max_time=1)

    pyautogui.sleep(2)
    click_icon("fuwawa", threshold=0.85)

    pyautogui.sleep(2)
    click_icon("confirm")

    pyautogui.sleep(2)
    pyautogui.click()

    pyautogui.sleep(2)
    click_icon("confirm")

    pyautogui.sleep(2)
    roll_gacha()

    end_time = time.time() + 3
    noel_here = imageDetect.findIconConfidenceCenter(r"C:\Users\Nathaniel Wan\Desktop\Programs\holodori_reroll\assets\swimsuit-noel.png")
    while time.time() < end_time:
        temp = imageDetect.findIconConfidenceCenter(r"C:\Users\Nathaniel Wan\Desktop\Programs\holodori_reroll\assets\swimsuit-noel.png")
        if temp[0] > noel_here[0]: 
            noel_here = temp
            print(f"noel here?? {noel_here} | {noel_here[0]>0.6}")
        if noel_here[0] > 0.6: exit()


    pyautogui.sleep(2)
    click_icon("blue-x")

    pyautogui.sleep(2)
    keyboard.press_and_release("space")
    pyautogui.sleep(2)
    keyboard.press("alt")
    pyautogui.sleep(2)
    click_icon("menu")
    pyautogui.sleep(2)
    keyboard.release("alt")


    pyautogui.sleep(0.2)
    click_icon("others")

    pyautogui.sleep(0.2)
    click_icon("title-screen")

    pyautogui.sleep(0.2)
    click_icon("yellow-ok")

    pyautogui.sleep(0.2)
    click_icon("title-menu")

    pyautogui.sleep(0.2)
    click_icon("title-language")

    pyautogui.sleep(0.2)
    click_icon("ok")

    pyautogui.sleep(0.5)
    pyautogui.scroll(-10000)
    pyautogui.sleep(0.2)
    click_icon("title-delete-account")
    pyautogui.sleep(0.2)
    click_icon("delete-proceed")
    pyautogui.sleep(0.2)
    click_icon("delete-final")
    pyautogui.sleep(0.2)
    click_icon("ok")
    pyautogui.sleep(2)

    print("done!")