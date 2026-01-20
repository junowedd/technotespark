PDF First Cover Page

[Technical Analysis] Connectivity-Aware Smart PCell
Script Name: my_rect_pcell.il

Framework: Cadence SKILL / ROD (Relative Object Design)

1. Executive Summary
This PCell (Parameterized Cell) is designed to automate the creation of a rectangular device layout with integrated connectivity. Unlike static layouts, this script implements "Correct-by-Construction" methodology by dynamically referencing technology rules and providing an interactive GUI for layout designers.

2. Key Functional Blocks
A. Dynamic Technology Rule Lookup
To ensure process portability and DRC compliance, the script avoids hard-coded values.

Mechanism: Uses techGetSpacingRule to query the PDK's Technology File.

Benefit: Automatically adapts to different process nodes (e.g., transitioning from 65nm to FinFET) by fetching the latest minWidth and minExtension rules for the MET1 layer.

B. Intelligent Object Management (ROD)
The script utilizes the ROD engine to create "named" objects rather than simple shapes.

Mechanism: rodCreateRect defines the body on the DIFF layer.

Benefit: Enables logical referencing of geometric points (e.g., centerRight, upperCenter) without manual coordinate calculation, ensuring robust alignment of secondary layers.

C. Self-Aligning Connectivity
Physical pins are mathematically linked to the parent geometry.

Mechanism: The MET1 pin is automatically centered at w/2.

Benefit: Maintains the logical terminal's integrity regardless of how the device is scaled, ensuring the cell remains LVS-clean at all times.

3. Technical Deep-Dive: rodAssignHandleToParameter
The most advanced feature of this PCell is its Interactive Stretch Handles, which bridge the gap between parameters and physical layout.

Relative Stretching: By using ?stretchType "relative", the script calculates the delta of the mouse movement, providing a fluid and intuitive user experience.

Origin Management: The ?moveOrigin t flag ensures that the cell's origin remains consistent even when the device is stretched from the negative axis, preventing hierarchical displacement.

Manufacturing Grid Enforcement (Snap Grid):

Implementation: ?snapSpacing 0.030

Purpose: Forces the stretch handles to align with the FinFET Fin Pitch. This prevents "Off-Grid" errors and ensures that the device dimensions are always quantized to legal manufacturing steps.

4. Conclusion & Design Impact
Efficiency: Reduces Layout Turn-Around Time (TAT) by replacing manual property editing with interactive on-canvas stretching.

Reliability: Eliminates human error by enforcing DRC rules and snap grids within the PCell's internal logic.

Scalability: The modular SKILL code serves as a template for more complex device generators (e.g., Multi-finger Transistors or Guard-rings).

💡 Interview Tip (English Phrase)
인터뷰에서 이 문서를 보여주며 이렇게 말씀해 보세요:

"I developed this PCell to demonstrate how SKILL automation can enforce design constraints early in the layout phase. By integrating snap grids and dynamic rule lookups, I've minimized the iteration loop between layout design and DRC verification."