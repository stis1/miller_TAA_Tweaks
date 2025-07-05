## All TAA values are stored inside taa_values.csv (CharaStencilMask and LiteMode doesn't work)
- To use this:
1. Open CMD or Terminal in this folder
2. Type "py NeedleFX_TAA_16_items.py taa_values.csv " and drag-n-drop all your RFL's in it
3. Now put new RFL's in your mod and it's done.

It seems that retail TAA was configured targeting 4K
I reconfigured it for 1080p and was targeting near MSAA 2x image

- jitterscale - How much TAA algorithm jitter pixels (1 - retail default, 0.25 - mod)
- sharpnesspower - Sharpness filter by TAA (not recommended to go higher than default 0.1)
- baseweight - Regulates how past frames influence new frame (low value for high influence, high value for low influence)
- velocityVarianceBasedWeightBias - How velocity influence past frame weight (step amount for following 2 params)
- velocityVarianceMin - Limits minimum weight 
- velocityVarianceMax - Limits maximum weight
- CharaStencilMask - Enables/Disables TAA for Shadow (Script doesn't change it)
- LiteMode - Enables/Disables TAA Lite Mode (Script doesn't change it)