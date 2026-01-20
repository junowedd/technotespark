/*****************************************************
* Report metal shapes on a given layer and net
*****************************************************/
procedure( reportMetalByNet( layerName netName )
  let( (cv count)
    cv = geGetEditCellView()

    unless( cv
      error("No editable cellview found.\n")
    )

    count = 0

    foreach( shape cv~>shapes
      when( shape~>layerName == layerName &&
            shape~>net &&
            shape~>net~>name == netName
        count = count + 1
      )
    )

    printf(
      "Layer %s, Net %s : %d shapes found\n"
      layerName netName count
    )

    count
  )
)

“I use logical AND with short-circuit evaluation in SKILL to safely check object properties, especially when database pointers such as nets can be nil.”
“The second condition prevents nil pointer errors by ensuring the net exists before accessing its name.”

/*****************************************************
* Check required text label existence
*****************************************************/
procedure( checkRequiredLabel( labelName )
  let( (cv missing)
    cv = geGetEditCellView()

    unless( cv
      error("No editable cellview found.\n")
    )

    missing = t

    foreach( shape cv~>shapes
      when( shape~>objType == "label" &&
            shape~>theLabel == labelName
        missing = nil
      )
    )

    if( missing then
      printf(
        "WARNING: Required label '%s' NOT found\n"
        labelName
      )
    else
      printf(
        "OK: Required label '%s' exists\n"
        labelName
      )
    )

    missing
  )
)


/*****************************************************
* Create a simple metal rectangle automatically
*****************************************************/
procedure( createMetalBar( layerName width height originX originY )
  let( (cv bbox)
    cv = geGetEditCellView()

    unless( cv
      error("No editable cellview found.\n")
    )

    bbox = list(
      originX
      originY
      originX + width
      originY + height
    )

    dbCreateRect(
      cv
      list( layerName "drawing" )
      bbox
    )

    printf(
      "Metal bar created on %s at (%d,%d)\n"
      layerName originX originY
    )
  )
)

“I usually separate reporting, checking, and automation utilities so that each script is reusable and easy to maintain across different technologies.”

“I focus on parameter-driven SKILL procedures to ensure scalability and easy adaptation to new PDK rules.”

Clean structure + reusable procedures + rule-driven logic 