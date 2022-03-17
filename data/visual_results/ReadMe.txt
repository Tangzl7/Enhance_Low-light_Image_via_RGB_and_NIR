The visual_results.zip file contains the visual results included in the main manuscript "Adaptive near-infrared and visible fusion for fast image enhancement",
and consists of two folders.

1. full_resolution_images_of_fig_3_and_4

Contains the full resolution images of Fig.3 and Fig.4 in the main manuscript.
Each image name follows the format ( fig_X_Y_WWW ), where
X 	---> 	represents the figure number (3 or 4)
Y 	---> 	represents the sub-figure indicator (a or b)
WWW	--->	represents an abbreviation for the image source, such as:
			rgb		---> for the original visible image
			nir 		---> for the near-infrared image used in the fusion
			CS		---> for the fused images obtained using the "channel swapping" fusion approach
			CPMM		---> for the fused images obtained using the "contrast-preserving mapping model" fusion approach
			SpE		---> for the fused images obtained using the "spectral edge" fusion approach
			WNTM		---> for the fused images obtained using the "weighted NIR using transmission map" fusion approach
			Proposed	---> for the fused images obtained using the proposed fusion approach

---------------------------------------------------------------------------------------------------------------------

2. results_of_synthetic_degradation_experiment

Contains the results of the synthetic degradation experiment discussed in Section V in the main manuscript,
and consists of two folders.
(a) degraded_vs_image: contains the visual results of the experiment when the visible image is synthetically degraded.
(b) degraded_nir_image: contains the visual results of the experiment when the near-infrared image is synthetically degraded.

Each image name in the two folders follows the format ( 92_XXX_Y_WWW ), where
X 	---> 	represents the type of the used degradation, such as:
			gwn	---> for Gaussian noise
			sap	---> for salt & pepper noise
			cmp	---> for compression artifacts
			blr	---> for blurriness
Y 	---> 	represents the parameter value used in the degradation (depends on the degradation type, please see Table S.V in the supplementary material document)
WWW	--->	represents an abbreviation for the image source, such as:
			rgb		---> for the degraded visible image used in the fusion (in folder "degraded_vs_image")
			nir 		---> for the degraded near-infrared image used in the fusion (in folder "degraded_nir_image")
			CS		---> for the fused images obtained using the "channel swapping" fusion approach
			CPMM		---> for the fused images obtained using the "contrast-preserving mapping model" fusion approach
			SpE		---> for the fused images obtained using the "spectral edge" fusion approach
			WNTM		---> for the fused images obtained using the "weighted NIR using transmission map" fusion approach
			Proposed	---> for the fused images obtained using the proposed fusion approach

The only two image names that do not follow the above format are:
92_rgb ... for the original visible image
92_nir ... for the original near-infrared image

Note that, the number (92) in all image names refer to the sample number that we selected form the dataset for the experiment.
