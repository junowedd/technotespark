[Technical Analysis] Connectivity-Aware Smart PCell
Script Name: my_rect_pcell.il

Core Framework: ROD (Relative Object Design) & Tech-File Driven Automation

1. PCell Definition & Parametrization
This section initializes the PCell and defines the user-adjustable parameters that drive the layout geometry. 
+1


Function: pcDefinePCell serves as the primary constructor for the cell. 
+1

Key Parameters:


w (float): Defines the device width (X-axis). 
+1


h (float): Defines the device height (Y-axis). 
+1


pinName (string): Assigns a unique logical identifier to the metal terminal. 
+1

2. Dynamic Tech-File Lookup (DRC-Awareness)
Rather than using hard-coded values, the script queries the library's Technology File to ensure the layout is "Correct-by-Construction." 
+1


Technology Access: techGetTechFile retrieves the specific design rules associated with the current library. 
+1


Rule Extraction: techGetSpacingRule dynamically fetches minWidth and minExtension for the MET1 layer. 
+1


Benefit: This ensures that the generated pin always complies with the minimum manufacturing requirements of the target process node. 
+1

3. Main Body Generation via ROD
The script utilizes the ROD (Relative Object Design) engine to create a high-level layout object. 
+1


Function: rodCreateRect generates a rectangle on the DIFF layer. 
+1


Object Mapping: By assigning a name (?name "body"), the script treats the rectangle as an intelligent object rather than just a collection of coordinates. 
+1


Advantage: Named objects allow for easy referencing of specific points (e.g., center, edges) for future alignment or secondary layer placement. 
+1

4. Interactive Stretch Handles
The script implements a Graphic User Interface (GUI) that allows designers to modify the device dimensions directly on the canvas. 
+1


Function: rodAssignHandleToParameter binds physical handles to the w and h parameters. 
+1


Intuitive Control: Handles such as centerRight and upperCenter allow for real-time stretching of the layout. 


Origin Management: The ?moveOrigin t flag ensures the PCell's origin updates correctly as the user stretches the device, preventing accidental offsets. 

5. Connectivity & Terminal Integration
The script bridges the gap between physical layout and logical netlist by creating functional pins. 
+1


Self-Aligning Pin: rodCreateRect on MET1 is mathematically centered at w/2, ensuring it remains perfectly aligned regardless of the device width. 
+1


Logical Connection: dbCreatePin assigns "terminal" status to the metal, making the PCell LVS-ready. 


Automated Labeling: dbCreateLabel adds a physical text identifier to the pin, improving visual navigation for the layout designer. 

💡 Key Presentation Talking Points (For the Interview)
PDK Independence: "By dynamically querying the tech-file, this PCell is node-agnostic. It automatically adapts to the design rules of whichever library it is instantiated in."

Design Efficiency: "The inclusion of stretch handles eliminates the need for manual coordinate entry in the properties window, significantly reducing layout turnaround time."

Connectivity Integrity: "The mathematical centering of the pin ensures that even if the device size is scaled, the connectivity remains robust and compliant with the schematic netlist."

Would you like me to create a "Technical Deep-Dive" section for the rodAssignHandleToParameter function, which is often the most impressive part for hiring managers? I can explain the different stretchType options (relative vs. absolute) if you'd like. Good luck with your interview at Infineon!