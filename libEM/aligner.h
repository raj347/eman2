/**
 * $Id$
 */
#ifndef eman__aligner_h__
#define eman__aligner_h__ 1


#include "emobject.h"
#include "transform.h"

namespace EMAN
{
	class EMData;
	class Cmp;

	/** Aligner class is the base class for all aligners. Each
     * specific Aligner type has a unique name. This name is used to
     * create a new Aligner instance or call an Aligner.
     *
     * Typical usage of Aligners:
     *
     * 1. How to get all the Aligner types
     *
     *    vector<string> all_aligners = Factory<Aligner>.get_list();
     *
     * 2. How to use an Aligner
     *
     *    EMData *img = ...;
     *    EMData *with = ...;
     *    img->align("ALIGNER_NAME", Dict("with", image1));
     *
     * 3. How to define a new Aligner class
     *
     *    A new XYZAligner class should implement the following functions:
     *
     *        EMData *align(EMData * this_img, string cmp_name = "") const;
     *        TypeDict get_param_types() const;
     *        string get_name() const { return "XYZ"; }
     *        static Aligner* NEW() { return new XYZAligner(); }
     */
	class Aligner
	{
	  public:
		virtual ~ Aligner()
		{
		}

		virtual EMData *align(EMData * this_img, string cmp_name = "") const = 0;

		virtual Dict get_params() const
		{
			return params;
		}

		virtual void set_params(const Dict & new_params)
		{
			params = new_params;
		}

		virtual TypeDict get_param_types() const = 0;
		virtual string get_name() const = 0;

	  protected:
		mutable Dict params;
	};

	/** Translational 2D Alignment using cross correlation.
     * It calculates the shift for a translational alignment, then
     * do the translation.
     */
	class TranslationalAligner:public Aligner
	{
	  public:
		EMData * align(EMData * this_img, string cmp_name = "") const;

		string get_name() const
		{
			return "Translational";
		}

		static Aligner *NEW()
		{
			return new TranslationalAligner();
		}

		TypeDict get_param_types() const
		{
			TypeDict d;
			  d.put("with", EMObject::EMDATA);
			  d.put("intonly", EMObject::INT);
			  d.put("maxshift", EMObject::INT);
			  d.put("useparent", EMObject::INT);
			  return d;
		}
	};

	/** Translational 3D Alignment using  cross correlation
     * It calculates the shift for a translational alignment, then
     * do the translation.
     */
	class Translational3DAligner:public Aligner
	{
	  public:
		EMData * align(EMData * this_img, string cmp_name = "") const;

		string get_name() const
		{
			return "Translational3D";
		}

		static Aligner *NEW()
		{
			return new Translational3DAligner();
		}

		TypeDict get_param_types() const
		{
			TypeDict d;
			  d.put("with", EMObject::EMDATA);
			  d.put("useparent", EMObject::INT);
			  return d;
		}

	};

	/** rotational alignment using angular correlation
     */
	class RotationalAligner:public Aligner
	{
	  public:
		EMData * align(EMData * this_img, string cmp_name = "") const;

		string get_name() const
		{
			return "Rotational";
		}

		static Aligner *NEW()
		{
			return new RotationalAligner();
		}

		TypeDict get_param_types() const
		{
			TypeDict d;
			  d.put("with", EMObject::EMDATA);
			  return d;
		}
	};

	/** rotational alignment assuming centers are correct
     */
	class RotatePrecenterAligner:public Aligner
	{
	  public:
		EMData * align(EMData * this_img, string cmp_name = "") const;

		string get_name() const
		{
			return "RotatePrecenter";
		}

		static Aligner *NEW()
		{
			return new RotatePrecenterAligner();
		}

		TypeDict get_param_types() const
		{
			TypeDict d;
			  d.put("with", EMObject::EMDATA);
			  return d;
		}
	};

	/** rotational alignment via circular harmonic
     */
	class RotateCHAligner:public Aligner
	{
	  public:
		EMData * align(EMData * this_img, string cmp_name = "") const;

		string get_name() const
		{
			return "RotateCH";
		}

		static Aligner *NEW()
		{
			return new RotateCHAligner();
		}

		TypeDict get_param_types() const
		{
			TypeDict d;
			  d.put("with", EMObject::EMDATA);
			  d.put("irad", EMObject::INT);
			  d.put("orad", EMObject::INT);
			  return d;
		}
	};

	/** rotational, translational alignment
     */
	class RotateTranslateAligner:public Aligner
	{
	  public:
		EMData * align(EMData * this_img, string cmp_name = "FRC") const;

		string get_name() const
		{
			return "RotateTranslate";
		}

		static Aligner *NEW()
		{
			return new RotateTranslateAligner();
		}

		TypeDict get_param_types() const
		{
			TypeDict d;
			  d.put("with", EMObject::EMDATA);
			  d.put("usedot", EMObject::INT);
			  d.put("maxshift", EMObject::INT);
			  return d;
		}
	};

	/** rotational, translational alignment
     */
	class RotateTranslateBestAligner:public Aligner
	{
	  public:
		EMData * align(EMData * this_img, string cmp_name = "FRC") const;

		string get_name() const
		{
			return "RotateTranslateBest";
		}

		static Aligner *NEW()
		{
			return new RotateTranslateBestAligner();
		}

		TypeDict get_param_types() const
		{
			TypeDict d;
			  d.put("with", EMObject::EMDATA);
			  d.put("maxshift", EMObject::INT);
			  d.put("snr", EMObject::FLOATARRAY);
			  return d;
		}
	};

	/** rotational, translational alignment with Radon transforms
     */
	class RotateTranslateRadonAligner:public Aligner
	{
	  public:
		EMData * align(EMData * this_img, string cmp_name = "") const;

		string get_name() const
		{
			return "RotateTranslateRadon";
		}

		static Aligner *NEW()
		{
			return new RotateTranslateRadonAligner();
		}

		TypeDict get_param_types() const
		{
			TypeDict d;
			  d.put("with", EMObject::EMDATA);
			  d.put("maxshift", EMObject::INT);
			  d.put("radonwith", EMObject::EMDATA);
			  d.put("radonthis", EMObject::EMDATA);
			  return d;
		}
	};

	/** rotational and flip alignment
     */
	class RotateFlipAligner:public Aligner
	{
	  public:
		EMData * align(EMData * this_img, string cmp_name = "") const;

		string get_name() const
		{
			return "RotateFlip";
		}

		static Aligner *NEW()
		{
			return new RotateFlipAligner();
		}

		TypeDict get_param_types() const
		{
			TypeDict d;
			  d.put("with", EMObject::EMDATA);
			  d.put("flip", EMObject::EMDATA);
			  d.put("imask", EMObject::INT);
			  return d;
		}
	};

	/** rotational, translational and flip alignment
     */
	class RotateTranslateFlipAligner:public Aligner
	{
	  public:
		EMData * align(EMData * this_img, string cmp_name = "Variance") const;

		string get_name() const
		{
			return "RotateTranslateFlip";
		}

		static Aligner *NEW()
		{
			return new RotateTranslateFlipAligner();
		}

		TypeDict get_param_types() const
		{
			TypeDict d;
			  d.put("with", EMObject::EMDATA);
			  d.put("flip", EMObject::EMDATA);
			  d.put("usedot", EMObject::INT);
			  d.put("maxshift", EMObject::INT);
			  return d;
		}
	};

	/** rotational, translational and flip alignment using real-space methods. slow
    */
	class RTFSlowAligner:public Aligner
	{
	  public:
		EMData * align(EMData * this_img, string cmp_name = "Variance") const;

		string get_name() const
		{
			return "RTFSlow";
		}

		static Aligner *NEW()
		{
			return new RTFSlowAligner();
		}

		TypeDict get_param_types() const
		{
			TypeDict d;
			  d.put("with", EMObject::EMDATA);
			  d.put("flip", EMObject::EMDATA);
			  d.put("maxshift", EMObject::INT);
			  return d;
		}
	};
	/** rotational, translational and flip alignment using exhaustive search. VERY SLOW
     */
	class RTFSlowestAligner:public Aligner
	{
	  public:
		EMData * align(EMData * this_img, string cmp_name = "Variance") const;

		string get_name() const
		{
			return "RTFSlowest";
		}

		static Aligner *NEW()
		{
			return new RTFSlowestAligner();
		}

		TypeDict get_param_types() const
		{
			TypeDict d;
			  d.put("with", EMObject::EMDATA);
			  d.put("flip", EMObject::EMDATA);
			  d.put("maxshift", EMObject::INT);
			  return d;
		}
	};

	/** rotational, translational and flip alignment using fscmp at multiple locations, slow
     * but this routine probably produces the best results
     */
	class RTFBestAligner:public Aligner
	{
	  public:
		EMData * align(EMData * this_img, string cmp_name = "FRC") const;

		string get_name() const
		{
			return "RTFBest";
		}

		static Aligner *NEW()
		{
			return new RTFBestAligner();
		}

		TypeDict get_param_types() const
		{
			TypeDict d;
			  d.put("with", EMObject::EMDATA);
			  d.put("flip", EMObject::EMDATA);
			  d.put("maxshift", EMObject::INT);
			  d.put("snr", EMObject::FLOATARRAY);
			  return d;
		}
	};

	/** rotational, translational and flip alignment with Radon transforms
     */
	class RTFRadonAligner:public Aligner
	{
	  public:
		EMData * align(EMData * this_img, string cmp_name = "Variance") const;

		string get_name() const
		{
			return "RTFRadon";
		}

		static Aligner *NEW()
		{
			return new RTFRadonAligner();
		}

		TypeDict get_param_types() const
		{
			TypeDict d;
			  d.put("with", EMObject::EMDATA);
			  d.put("maxshift", EMObject::INT);
			  d.put("thisf", EMObject::EMDATA);
			  d.put("radonwith", EMObject::EMDATA);
			  d.put("radonthis", EMObject::EMDATA);
			  d.put("radonthisf", EMObject::EMDATA);
			  return d;
		}
	};

	/** refine alignment
     */
	class RefineAligner:public Aligner
	{
	  public:
		EMData * align(EMData * this_img, string cmp_name = "FRC") const;

		string get_name() const
		{
			return "Refine";
		}

		static Aligner *NEW()
		{
			return new RefineAligner();
		}

		TypeDict get_param_types() const
		{
			TypeDict d;
			  d.put("with", EMObject::EMDATA);
			  d.put("mode", EMObject::INT);
			  d.put("snr", EMObject::FLOATARRAY);
			  d.put("alot", EMObject::FLOAT);
			  d.put("az", EMObject::FLOAT);
			  d.put("phi", EMObject::FLOAT);
			  d.put("dx", EMObject::FLOAT);
			  d.put("dy", EMObject::FLOAT);
			  d.put("dz", EMObject::FLOAT);


			  return d;
		}
	};

	template <> Factory < Aligner >::Factory();

	void dump_aligners();

}

#endif
