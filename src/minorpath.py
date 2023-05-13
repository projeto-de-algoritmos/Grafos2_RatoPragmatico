from tkinter import *
from PIL import ImageTk, Image

def dijikstra(queue,start_box, target_box, searching, path):
      
        if len(queue) > 0 and searching:
                current_box = queue.pop(0)
                current_box.visited = True
                if current_box == target_box:
                    searching = False
                    while current_box.prior != start_box:
                        path.append(current_box.prior)
                        current_box = current_box.prior
                else:
                    for neighbour in current_box.neighbours:
                        if not neighbour.queued and not neighbour.wall:
                            neighbour.queued = True
                            neighbour.prior = current_box
                            queue.append(neighbour)        
        else:
            if searching:
                        show_lose_window("assets/losegame.png")
                        return False
        return searching


def show_lose_window(lose):
    root = Tk()
    root.geometry("350x350")
    root.title("Seu rato vai passar fome!")
    image = Image.open(lose)
    photo = ImageTk.PhotoImage(image)
    
    image_label = Label(root, image=photo)
    image_label.pack()
    
    text_label = Label(root, text="Seu rato vai passar fome!")
    text_label.pack()
    
    root.mainloop()

def show_win_window(win):
    root = Tk()
    root.geometry("350x350")
    root.title("Achou o queijo!")
    image = Image.open(win)
    photo = ImageTk.PhotoImage(image)
    
    image_label = Label(root, image=photo)
    image_label.pack()
    
    text_label = Label(root, text="Achou o queijo!")
    text_label.pack()
    
    root.mainloop()
              

