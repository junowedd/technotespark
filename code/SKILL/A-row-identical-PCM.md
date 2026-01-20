Write a simple SKILL procedure that generates
a row of identical PCM structures in a layout cellview.

Each structure should be placed with a fixed pitch
and controlled by parameters.


procedure(createPCMArray(cv numDevices pitch)
  let((i xOffset)

    xOffset = 0

    for(i 0 numDevices-1
      dbCreateRect(
        cv
        "M1"
        list(
          xOffset:0
          xOffset+0.2:0.2
        )
      )
      xOffset = xOffset + pitch
    )
  )
)

How would you prevent invalid PCM configurations using SKILL?

procedure(checkPCMParameters(numDevices pitch)
  when(numDevices < 2
    error("PCM array must have at least 2 devices")
  )

  when(pitch < 0.3
    error("Pitch violates minimum DFM spacing")
  )
)

How would you structure this as a PCell?

pcDefinePCell(
  list(ddGetObj("TestLib") "pcm_array" "layout")
  (
    (numDevices 4)
    (pitch 0.4)
  )
  let((cv)
    cv = pcCellView
    checkPCMParameters(numDevices pitch)
    createPCMArray(cv numDevices pitch)
  )
)

“I separate parameter validation from geometry generation
so the methodology can scale.”

I focus on preventing invalid layout creation at the automation level.
For testchips and PCM, this is more effective than relying solely on DRC,
especially when structures are repeated across wafers.

I would remove continuous geometry freedom
and move to discrete, grid-based parameters,
especially for FinFET-related PCM structures.