import glob
from PIL import Image

def make_gif(frame_folder):
    frames = [Image.open(image) for image in sorted(glob.glob(f"{frame_folder}/*.PNG"))]
    frame_one = frames[0]
    f = frame_folder.split("\\")[-1]
    frame_one.save(f"{f}.gif", format="GIF", append_images=frames,
               save_all=True, duration=0.1)

for i in range(16):   
    if __name__ == "__main__":
        make_gif(f"C:\DLA-master\gif{i}")
