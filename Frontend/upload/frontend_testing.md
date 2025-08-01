#  Frontend Testing Documentation

This document outlines the **manual testing procedures** and **test coverage** for the frontend of the **BioData 3D Viewer**. The frontend is built in HTML, CSS, and JavaScript, and communicates with a Flask backend.

---

##  Features to be Tested

| Feature                     | Description                                                                 | Tested |
|---------------------------- |-----------------------------------------------------------------------------|--------|
|  Model List Rendering       | Correctly fetches and renders all uploaded `.stl` and `.obj` model names.   | ✅     |
|  Load Model                 | Clicking a filename loads the model in the 3D viewport.                     | ✅     |
|  Add Landmark               | User can click on the 3D model to place a labeled landmark.                 | ✅     |
|  Delete Landmark            | Landmark can be deleted in delete mode.                                     | ✅     |
|  Move Landmark              | Landmark can be dragged to new position.                                    | ✅ (with drift) |
|  Set Coordinate Origin      | Select a landmark to set it as origin.                                      | ✅     |
|  Draw Coordinate Axes       | XYZ axes appear after setting origin.                                       | ✅     |
|  Show Relative Coordinates  | Landmark list shows coordinates relative to origin.                         | ✅     |
|  Theme Toggle               | Switch between light and dark theme.                                        | ✅     |
|  Delete Model               | Delete model using trash icon.                                              | ✅     |
|  Edge Case Handling         | Click outside model, delete origin, etc.                                    | ✅     |

---

##  Manual Test Cases

###  Test 1: Model Loading

**Steps**:
1. Upload `.stl` or `.obj` file.
2. Click filename in model list.

**Expected Result**:
Model renders correctly in the viewer.

---

###  Test 2: Add Landmark

**Steps**:
1. Enable `landmark mode`.
2. Click on the 3D model.
3. Enter the ID of the landmark.
4. Landmark appear.

**Expected Result**:
A labeled point appears with unique ID.

---

###  Test 3: Delete Landmark

**Steps**:
1. Enable `delete mode`.
2. Click on a landmark.

**Expected Result**:
The landmark disappears.
If the landmark is the originpoint of the coordinate system, a warning will raise and forbidden the request.

---

###  Test 4: Move Landmark

**Steps**:
1. Enable `move mode`.
2. Click and drag a landmark.

**Expected Result**:
Landmark moves correctly along surface.

**Current Issue**:
Landmark may drift off the model surface.

---

###  Test 5: Coordinate System

**Steps**:
1. Enable `coordinate mode`.
2. Click on a landmark.

**Expected Result**:
Origin is set and axes appear.
All landmarks will refresh the them locations based on the new axes.
If the originpoint move the coordinate system will move with the point.

---

###  Test 6: Theme & Mode UI

- Toggle theme.
- Switch between modes.
- Confirm only one mode is active.

---

###  Test 7: Save model

**Steps**:
1. Click the “Save as Obj” or “Save as stl” button on the page to save the current model state.
2. If the current model contains new changes:
   - The system should package all landmark changes into a new file (e.g., `.stl`, `.obj`).
3. Enter name for new model.
4. Save model.


**Expected Result**:
- The user can successfully save the model.
- The new model appear directly in the list.
- The filename should be the written one.
- If users try to save .obj as .stl, a warning will appear.
---

###  Test 8: Delete Models

**Steps**:
1. Click a model
2. Click `delete model`.

**Expected Result**:
The chosen model disappears.
The model list will refresh.

---

###  Test 9: Delete Models

**Steps**:
1. Click the “Measure Distance” mode button to enable distance measuring mode.
2. Select two existing landmark points on the model surface.
3. The distance (in appropriate units) should be displayed in distance list panel.

**Expected Result**:
- Distance mode activates correctly and UI indicates it is active.
- The distance between the two points is accurately calculated and displayed.
- UI remains responsive while switching between other modes (e.g., landmark mode, move mode).

##  Known Issues

| Issue                 | Description                                            | Severity |
|----------------------|--------------------------------------------------------|----------|
| Landmark Drift        | Dragged landmark may not stick to model surface        | Medium   |
| Coordinate Reset Bug  | Clicking same origin twice may not reset properly      | Low      |
| Label Overlap         | Close landmarks cause label overlap                    | Low      |

---

##  Improvement Suggestions

- Use mesh-projected raycasting for drag accuracy.
- Enable 3-point selection for full coordinate system.
- Add undo/redo support.
- Improve landmark collision detection.


---

##  Final Notes

- All tests above have been manually verified.
- Automated UI testing (e.g., Cypress) is not implemented yet.
- Video demonstrations can be included for clarity in assessment.



