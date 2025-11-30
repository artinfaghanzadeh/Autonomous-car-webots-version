📦Autonomous-car-webots-version
 ┣ 📂.git
 ┣ 📂config
 ┃ ┣ 📜__init__.py
 ┃ ┣ 📜debug.yaml
 ┃ ┣ 📜debug_config.py
 ┃ ┣ 📜statics.py
 ┃ ┣ 📜statics.yaml
 ┃ ┣ 📜ui.yaml
 ┃ ┗ 📜ui_config.py
 ┣ 📂docs
 ┃ ┣ 📂media
 ┃ ┃ ┗ 📜architecture_flowchart.png
 ┃ ┣ 📜architecture.md
 ┃ ┣ 📜dev_notes.md
 ┃ ┣ 📜pipeline_lanes.md
 ┃ ┗ 📜usage.md
 ┣ 📂logs
 ┃ ┣ 📂events
 ┃ ┣ 📂performance
 ┃ ┗ 📂runtime
 ┣ 📂src
 ┃ ┣ 📂adjust_data
 ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┣ 📜camera_filter.py
 ┃ ┃ ┗ 📜sensor_filter.py
 ┃ ┣ 📂common
 ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┣ 📜control_command.py
 ┃ ┃ ┣ 📜perception_state.py
 ┃ ┃ ┗ 📜vehicle_state.py
 ┃ ┣ 📂config
 ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┣ 📜statics.py
 ┃ ┃ ┗ 📜ui_config.py
 ┃ ┣ 📂core
 ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┗ 📜core.py
 ┃ ┣ 📂executive
 ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┣ 📜commands.py
 ┃ ┃ ┣ 📜pid_speed.py
 ┃ ┃ ┗ 📜pid_steering.py
 ┃ ┣ 📂fw_debug
 ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┣ 📜camera_overlay.py
 ┃ ┃ ┣ 📜exec_realtime.py
 ┃ ┃ ┣ 📜exec_recorded.py
 ┃ ┃ ┣ 📜logic_overlay.py
 ┃ ┃ ┣ 📜pose_overlay.py
 ┃ ┃ ┣ 📜safety_overlay.py
 ┃ ┃ ┗ 📜sensor_overlay.py
 ┃ ┣ 📂get_data
 ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┣ 📜camera.py
 ┃ ┃ ┣ 📜raw_sensor.py
 ┃ ┃ ┗ 📜wheel.py
 ┃ ┣ 📂logic
 ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┣ 📜fuser.py
 ┃ ┃ ┣ 📜lanes_behavior.py
 ┃ ┃ ┣ 📜object_behavior.py
 ┃ ┃ ┣ 📜qr_behavior.py
 ┃ ┃ ┗ 📜roads_behavior.py
 ┃ ┣ 📂process
 ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┣ 📜lanes_detection.py
 ┃ ┃ ┣ 📜object_detection.py
 ┃ ┃ ┣ 📜pose_detection.py
 ┃ ┃ ┣ 📜qr_detection.py
 ┃ ┃ ┗ 📜roads_detection.py
 ┃ ┣ 📂safety
 ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┗ 📜exception_guard.py
 ┃ ┗ 📜__init__.py
 ┣ 📂tests
 ┃ ┣ 📜__init__.py
 ┃ ┣ 📜test_camera_filter.py
 ┃ ┣ 📜test_lanes_detections.py
 ┃ ┗ 📜test_pid.py
 ┣ 📂webots
 ┃ ┣ 📂controllers
 ┃ ┃ ┗ 📂controller_2
 ┃ ┃ ┃ ┗ 📜controller_2.py
 ┃ ┣ 📂libraries
 ┃ ┣ 📂plugins
 ┃ ┃ ┣ 📂physics
 ┃ ┃ ┣ 📂remote_controls
 ┃ ┃ ┗ 📂robot_windows
 ┃ ┣ 📂protos
 ┃ ┃ ┣ 📂icons
 ┃ ┃ ┃ ┗ 📜CurvedRoadSegment.png
 ┃ ┃ ┗ 📜CurvedRoadSegment.proto
 ┃ ┗ 📂worlds
 ┃ ┃ ┣ 📜.city.jpg
 ┃ ┃ ┣ 📜.city.wbproj
 ┃ ┃ ┣ 📜.highway.jpg
 ┃ ┃ ┣ 📜.highway.wbproj
 ┃ ┃ ┣ 📜.main.wbproj
 ┃ ┃ ┣ 📜city.wbt
 ┃ ┃ ┣ 📜highway.wbt
 ┃ ┃ ┗ 📜main.wbt
 ┣ 📜.gitignore
 ┣ 📜LICENSE
 ┣ 📜README.md
 ┗ 📜requirements.txt