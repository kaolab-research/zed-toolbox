'''
In this example, there are two cameras in the environments.
The live view of camera 1 is enabled but no recording from there.
An overlay of a moving dot is added in camera 2 but no live view.
'''
import time
from zed_toolbox.system import CameraSystem


def main():

    # ===== YOUR CHANGES =====
    serial1 = 24944966
    serial2 = 33261276

    # see readme for full configurations.
    cam1_config = {
        "enable_viewer": True,
        "enable_recorder": False,

        "specifications": {
            "fps": 30,
            "auto_exposure": False,
            "exposure": 20,
            "gain": 50,
        },

        "viewer": {
            "show_color": True,
            "show_depth": False,
            "fps": 30
        },
    }
    cam2_config = {
        "enable_viewer": True,
        "enable_recorder": False,

        "specifications": {
            "fps": 30,
            "auto_exposure": False,
            "exposure": 25,
            "gain": 45,
        },

        "viewer": {
            "show_color": True,
            "show_depth": False,
            "fps": 30
        },
    }
    # ========================

    system_config = {
        serial1: cam1_config, 
        serial2: cam2_config
    }

    system = None
    try:
        system = CameraSystem(system_config=system_config)
        system.launch()

        while True:

            moving_x = int(100 + 50 * (1 + time.time() % 4))
            
            # see readme for full configurations.
            overlays = [
                {
                    "type": "dot",
                    "xy": (moving_x, 200),
                    # "radius": 8,
                    # "color": (0, 255, 0) # Green
                }
            ]
            all_overlays = {serial2: overlays}
            
            all_frames = system.update(all_overlays)

            if not system.is_alive:
                break

            if all_frames:
                print(f"--- Frame Batch Received ({time.strftime('%H:%M:%S')}) ---")
                for serial, state in all_frames.items():
                    print(f"  Camera [{serial}]: Color={state['left_image'].shape}, Depth={state['depth'].shape}")

    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Exiting gracefully.")

    except Exception as e:
        print(f"Unexpected error occurred: {e}")

    finally:
        system.shutdown()



if __name__ == "__main__":
    main()