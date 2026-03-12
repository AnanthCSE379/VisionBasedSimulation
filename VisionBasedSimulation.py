import cv2  
import numpy as np 
import time
import sys 
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

print('Program started')

try:
    client = RemoteAPIClient(port = 23000)
    print("Successfully connected to ZMQ server.")
except Exception as e:
    print(f"Connection failed: {e}")
    sys.exit() # Exit if we can't connect

sim = client.getObject('sim')

try:
    motorC = sim.getObject('/RRwheel_motor')
    motorD = sim.getObject('/RLwheel_motor')
    camera = sim.getObject('/visionSensor') 
    
    if motorC == -1 or motorD == -1 or camera == -1:
        raise Exception("Could not get all object handles. Check names in CoppeliaSim.")
        
    print('Connected to robot. Starting simulation...')

    try:
        sim.startSimulation()
        vel = 1 # Set your desired speed
        
        start_time = time.time()
        sim.setJointTargetVelocity(motorC, -vel)
        sim.setJointTargetVelocity(motorD, +vel)
        
        while time.time() - start_time < 15:
            # 1. Get the image from the camera
            img, lst = sim.getVisionSensorImg(camera)
            
            if img:
                # 2. Process the image
                img_np = np.frombuffer(img, dtype=np.uint8).reshape((lst[0], lst[1], 3))
                img_np = cv2.flip(img_np, 0) # Flip vertically
                img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR) # Convert RGB to BGR
                
                # 3. Perform Edge Detection
                gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY) 
                edges = cv2.Canny(gray, 50, 150) 
                
                # 4. Display the images
                cv2.imshow('Robot View', img_np)
                cv2.imshow('Edge Detection', edges)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("'q' pressed. Emergency stop 'negotiated'.")
                    break 

        print("STOPPING...")
        sim.setJointTargetVelocity(motorC, 0)
        sim.setJointTargetVelocity(motorD, 0)
        sim.stopSimulation()
        print('Program ended')
        
    except Exception as e:
        print(f"An error occurred during simulation: {e}")
        sim.stopSimulation() # Ensure simulation stops on error
        
    finally:
        # This "cleans up" all "actuators" after the "mission"
        cv2.destroyAllWindows() 
        
except Exception as e:
    print(f"Exception occurred in main block: {e}")

# We add one final waitKey xjust in case windows need cleanup time
cv2.waitKey(1)
cv2.destroyAllWindows()