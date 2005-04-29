
// Boost Includes ==============================================================
#include <boost/python.hpp>
#include <boost/cstdint.hpp>

// Includes ====================================================================
#include <aligner.h>
#include <all_imageio.h>
#include <cmp.h>
#include <ctf.h>
#include <emdata.h>
#include <emfft.h>
#include <filter.h>
#include <transform.h>
#include <xydata.h>

// Using =======================================================================
using namespace boost::python;

// Declarations ================================================================
namespace  {

BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(EMAN_EMData_read_image_overloads_1_5, read_image, 1, 5)

BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(EMAN_EMData_write_image_overloads_1_7, write_image, 1, 7)

BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(EMAN_EMData_append_image_overloads_1_3, append_image, 1, 3)

BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(EMAN_EMData_write_lst_overloads_1_4, write_lst, 1, 4)

BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(EMAN_EMData_filter_overloads_1_2, process, 1, 2)

BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(EMAN_EMData_align_overloads_2_4, align, 2, 4)

BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(EMAN_EMData_project_overloads_1_2, project, 1, 2)

BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(EMAN_EMData_copy_overloads_0_1, copy, 0, 1)

BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(EMAN_EMData_get_rotated_clip_overloads_2_3, get_rotated_clip, 2, 3)

BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(EMAN_EMData_insert_scaled_sum_overloads_2_4, insert_scaled_sum, 2, 4)

BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(EMAN_EMData_zeropad_ntimes_overloads_0_1, zeropad_ntimes, 0, 1)

BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(EMAN_EMData_pad_fft_overloads_0_1, pad_fft, 0, 1)

BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(EMAN_EMData_little_big_dot_overloads_1_2, little_big_dot, 1, 2)

BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(EMAN_EMData_calc_ccf_overloads_1_3, calc_ccf, 1, 3)

BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(EMAN_EMData_calc_ccfx_overloads_1_4, calc_ccfx, 1, 4)

BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(EMAN_EMData_make_rotational_footprint_overloads_0_2, make_rotational_footprint, 0, 2)

BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(EMAN_EMData_calc_mutual_correlation_overloads_1_3, calc_mutual_correlation, 1, 3)

BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(EMAN_EMData_unwrap_overloads_0_6, unwrap, 0, 6)

BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(EMAN_EMData_apply_radial_func_overloads_3_4, apply_radial_func, 3, 4)

BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(EMAN_EMData_add_overloads_1_2, add, 1, 2)

BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(EMAN_EMData_calc_hist_overloads_1_4, calc_hist, 1, 4)

BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(EMAN_EMData_calc_dist_overloads_1_2, calc_dist, 1, 2)

BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(EMAN_EMData_calc_flcf_overloads_1_3, calc_flcf, 1, 3)

BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(EMAN_EMData_dot_overloads_1_2, dot, 1, 2)

BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(EMAN_EMData_common_lines_overloads_2_5, common_lines, 2, 5)

BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(EMAN_EMData_common_lines_real_overloads_2_4, common_lines_real, 2, 4)

BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(EMAN_EMData_cut_slice_overloads_2_6, cut_slice, 2, 6)

BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(EMAN_EMData_uncut_slice_overloads_2_5, uncut_slice, 2, 5)

BOOST_PYTHON_FUNCTION_OVERLOADS(EMAN_EMData_read_images_overloads_1_3, EMAN::EMData::read_images, 1, 3)

BOOST_PYTHON_FUNCTION_OVERLOADS(EMAN_EMData_read_images_ext_overloads_3_5, EMAN::EMData::read_images_ext, 3, 5)


}// namespace 


// Module ======================================================================
BOOST_PYTHON_MODULE(libpyEMData2)
{
    scope* EMAN_EMData_scope = new scope(
    class_< EMAN::EMData >("EMData", init<  >())
        .def(init< const EMAN::EMData& >())
        .def("read_image", &EMAN::EMData::read_image, EMAN_EMData_read_image_overloads_1_5())
        .def("write_image", &EMAN::EMData::write_image, EMAN_EMData_write_image_overloads_1_7())
        .def("append_image", &EMAN::EMData::append_image, EMAN_EMData_append_image_overloads_1_3())
        .def("write_lst", &EMAN::EMData::write_lst, EMAN_EMData_write_lst_overloads_1_4())
        .def("process", &EMAN::EMData::process, EMAN_EMData_filter_overloads_1_2())
        .def("cmp", &EMAN::EMData::cmp)
        .def("align", &EMAN::EMData::align, EMAN_EMData_align_overloads_2_4()[ return_value_policy< manage_new_object >() ])
        .def("project", &EMAN::EMData::project, EMAN_EMData_project_overloads_1_2()[ return_value_policy< manage_new_object >() ])
        .def("copy", &EMAN::EMData::copy, EMAN_EMData_copy_overloads_0_1()[ return_value_policy< manage_new_object >() ])
        .def("copy_head", &EMAN::EMData::copy_head, return_value_policy< manage_new_object >())
        .def("get_clip", &EMAN::EMData::get_clip, return_value_policy< manage_new_object >())
        .def("insert_clip", &EMAN::EMData::insert_clip)
        .def("get_top_half", &EMAN::EMData::get_top_half, return_value_policy< manage_new_object >())
        .def("get_rotated_clip", &EMAN::EMData::get_rotated_clip, EMAN_EMData_get_rotated_clip_overloads_2_3()[ return_value_policy< manage_new_object >() ])
        .def("insert_scaled_sum", &EMAN::EMData::insert_scaled_sum, EMAN_EMData_insert_scaled_sum_overloads_2_4())
        .def("window_padded", &EMAN::EMData::window_padded, return_value_policy< manage_new_object >())
        .def("center_origin_fft", &EMAN::EMData::center_origin_fft)
        .def("zeropad_ntimes", &EMAN::EMData::zeropad_ntimes, EMAN_EMData_zeropad_ntimes_overloads_0_1()[ return_value_policy< manage_new_object >() ])
        .def("pad_fft", &EMAN::EMData::pad_fft, EMAN_EMData_pad_fft_overloads_0_1()[ return_value_policy< manage_new_object >() ])
        .def("do_fft", &EMAN::EMData::do_fft, return_value_policy< manage_new_object >())
        .def("do_fft_inplace", &EMAN::EMData::do_fft_inplace, return_value_policy< reference_existing_object >())
        .def("do_ift", &EMAN::EMData::do_ift, return_value_policy< manage_new_object >())
        .def("do_ift_inplace", &EMAN::EMData::do_ift_inplace, return_value_policy< reference_existing_object >())
        .def("get_fft_amplitude", &EMAN::EMData::get_fft_amplitude, return_value_policy< manage_new_object >())
        .def("get_fft_phase", &EMAN::EMData::get_fft_phase, return_value_policy< manage_new_object >())
        .def("normalize_slice", (EMAN::FloatPoint (EMAN::EMData::*)(EMAN::EMData*, const EMAN::Transform3D&) )&EMAN::EMData::normalize_slice)
        .def("normalize_slice", (EMAN::FloatPoint (EMAN::EMData::*)(EMAN::EMData*, float, float, float) )&EMAN::EMData::normalize_slice)
        .def("render_amp8", &EMAN::EMData::render_amp8)
        .def("ri2ap", &EMAN::EMData::ri2ap)
        .def("ap2ri", &EMAN::EMData::ap2ri)
        .def("scale", &EMAN::EMData::scale)
        .def("translate", (void (EMAN::EMData::*)(float, float, float) )&EMAN::EMData::translate)
        .def("translate", (void (EMAN::EMData::*)(const EMAN::Vec3f&) )&EMAN::EMData::translate)
        .def("rotate", (void (EMAN::EMData::*)(const EMAN::Transform3D&) )&EMAN::EMData::rotate)
        .def("rotate", (void (EMAN::EMData::*)(float, float, float) )&EMAN::EMData::rotate)
        .def("rotate_translate", (void (EMAN::EMData::*)(const EMAN::Transform3D&) )&EMAN::EMData::rotate_translate)
        .def("rotate_translate", (void (EMAN::EMData::*)(float, float, float, float, float, float) )&EMAN::EMData::rotate_translate)
        .def("rotate_translate", (void (EMAN::EMData::*)(float, float, float, float, float, float, float, float, float) )&EMAN::EMData::rotate_translate)
        .def("rotate_x", &EMAN::EMData::rotate_x)
        .def("rotate_180", &EMAN::EMData::rotate_180)
        .def("dot_rotate_translate", &EMAN::EMData::dot_rotate_translate)
        .def("little_big_dot", &EMAN::EMData::little_big_dot, EMAN_EMData_little_big_dot_overloads_1_2()[ return_value_policy< manage_new_object >() ])
        .def("do_radon", &EMAN::EMData::do_radon, return_value_policy< manage_new_object >())
        .def("calc_ccf", &EMAN::EMData::calc_ccf, EMAN_EMData_calc_ccf_overloads_1_3()[ return_value_policy< manage_new_object >() ])
        .def("calc_ccfx", &EMAN::EMData::calc_ccfx, EMAN_EMData_calc_ccfx_overloads_1_4()[ return_value_policy< manage_new_object >() ])
        .def("make_rotational_footprint", &EMAN::EMData::make_rotational_footprint, EMAN_EMData_make_rotational_footprint_overloads_0_2()[ return_internal_reference< 1 >() ])
        .def("calc_mutual_correlation", &EMAN::EMData::calc_mutual_correlation, EMAN_EMData_calc_mutual_correlation_overloads_1_3()[ return_value_policy< manage_new_object >() ])
        .def("unwrap", &EMAN::EMData::unwrap, EMAN_EMData_unwrap_overloads_0_6()[ return_value_policy< manage_new_object >() ])
        .def("mean_shrink", &EMAN::EMData::mean_shrink)
        .def("median_shrink", &EMAN::EMData::median_shrink)
        .def("apply_radial_func", &EMAN::EMData::apply_radial_func, EMAN_EMData_apply_radial_func_overloads_3_4())
        .def("calc_radial_dist", (std::vector<float,std::allocator<float> > (EMAN::EMData::*)(int, float, float) )&EMAN::EMData::calc_radial_dist)
        .def("calc_radial_dist", (std::vector<float,std::allocator<float> > (EMAN::EMData::*)(int, float, float, float, float) )&EMAN::EMData::calc_radial_dist)
        .def("add", (void (EMAN::EMData::*)(float, int) )&EMAN::EMData::add, EMAN_EMData_add_overloads_1_2())
        .def("add", (void (EMAN::EMData::*)(const EMAN::EMData&) )&EMAN::EMData::add)
        .def("sub", (void (EMAN::EMData::*)(float) )&EMAN::EMData::sub)
        .def("sub", (void (EMAN::EMData::*)(const EMAN::EMData&) )&EMAN::EMData::sub)
        .def("mult", (void (EMAN::EMData::*)(int) )&EMAN::EMData::mult)
        .def("mult", (void (EMAN::EMData::*)(float) )&EMAN::EMData::mult)
        .def("mult", (void (EMAN::EMData::*)(const EMAN::EMData&) )&EMAN::EMData::mult)
        .def("div", (void (EMAN::EMData::*)(float) )&EMAN::EMData::div)
        .def("div", (void (EMAN::EMData::*)(const EMAN::EMData&) )&EMAN::EMData::div)
        .def("set_shared_data", &EMAN::EMData::set_shared_data)
        .def("done_data", &EMAN::EMData::done_data)
        .def("update", &EMAN::EMData::update)
        .def("to_zero", &EMAN::EMData::to_zero)
        .def("to_one", &EMAN::EMData::to_one)
        .def("add_incoherent", &EMAN::EMData::add_incoherent)
        .def("calc_fourier_shell_correlation", &EMAN::EMData::calc_fourier_shell_correlation)
        .def("calc_hist", &EMAN::EMData::calc_hist, EMAN_EMData_calc_hist_overloads_1_4())
        .def("calc_az_dist", &EMAN::EMData::calc_az_dist)
        .def("calc_dist", &EMAN::EMData::calc_dist, EMAN_EMData_calc_dist_overloads_1_2())
        .def("calc_flcf", &EMAN::EMData::calc_flcf, EMAN_EMData_calc_flcf_overloads_1_3()[ return_value_policy< manage_new_object >() ])
        .def("convolute", &EMAN::EMData::convolute, return_value_policy< manage_new_object >())
        .def("has_ctff", &EMAN::EMData::has_ctff)
        .def("dot", &EMAN::EMData::dot, EMAN_EMData_dot_overloads_1_2())
        .def("common_lines", &EMAN::EMData::common_lines, EMAN_EMData_common_lines_overloads_2_5())
        .def("common_lines_real", &EMAN::EMData::common_lines_real, EMAN_EMData_common_lines_real_overloads_2_4())
        .def("cut_slice", &EMAN::EMData::cut_slice, EMAN_EMData_cut_slice_overloads_2_6())
        .def("uncut_slice", &EMAN::EMData::uncut_slice, EMAN_EMData_uncut_slice_overloads_2_5())
        .def("calc_center_density", &EMAN::EMData::calc_center_density)
        .def("calc_sigma_diff", &EMAN::EMData::calc_sigma_diff)
        .def("calc_min_location", &EMAN::EMData::calc_min_location)
        .def("calc_max_location", &EMAN::EMData::calc_max_location)
        .def("calc_min_index", &EMAN::EMData::calc_min_index)
        .def("calc_max_index", &EMAN::EMData::calc_max_index)
        .def("calc_highest_locations", &EMAN::EMData::calc_highest_locations)
        .def("get_edge_mean", &EMAN::EMData::get_edge_mean)
        .def("get_circle_mean", &EMAN::EMData::get_circle_mean)
        .def("setup_insert_slice", &EMAN::EMData::setup_insert_slice)
        .def("get_ctf", &EMAN::EMData::get_ctf, return_internal_reference< 1 >())
        .def("set_ctf", &EMAN::EMData::set_ctf)
        .def("get_translation", &EMAN::EMData::get_translation)
        .def("set_translation", (void (EMAN::EMData::*)(const EMAN::Vec3f&) )&EMAN::EMData::set_translation)
        .def("set_translation", (void (EMAN::EMData::*)(float, float, float) )&EMAN::EMData::set_translation)
        .def("get_transform", &EMAN::EMData::get_transform)
        .def("set_rotation", &EMAN::EMData::set_rotation)
        .def("set_size", &EMAN::EMData::set_size)
        .def("set_complex_size", &EMAN::EMData::set_complex_size)
        .def("set_path", &EMAN::EMData::set_path)
        .def("set_pathnum", &EMAN::EMData::set_pathnum)
        .def("get_2dview", (EMAN::MArray2D (EMAN::EMData::*)() const)&EMAN::EMData::get_2dview)
        .def("get_3dview", (EMAN::MArray3D (EMAN::EMData::*)() const)&EMAN::EMData::get_3dview)
        .def("get_2dcview", (EMAN::MCArray2D (EMAN::EMData::*)() const)&EMAN::EMData::get_2dcview)
        .def("get_3dcview", (EMAN::MCArray3D (EMAN::EMData::*)() const)&EMAN::EMData::get_3dcview)
        .def("get_2dview", (EMAN::MArray2D (EMAN::EMData::*)(int, int) const)&EMAN::EMData::get_2dview)
        .def("get_3dview", (EMAN::MArray3D (EMAN::EMData::*)(int, int, int) const)&EMAN::EMData::get_3dview)
        .def("get_2dcview", (EMAN::MCArray2D (EMAN::EMData::*)(int, int) const)&EMAN::EMData::get_2dcview)
        .def("get_3dcview", (EMAN::MCArray3D (EMAN::EMData::*)(int, int, int) const)&EMAN::EMData::get_3dcview)
        .def("get_row", &EMAN::EMData::get_row, return_value_policy< manage_new_object >())
        .def("set_row", &EMAN::EMData::set_row)
        .def("get_col", &EMAN::EMData::get_col, return_value_policy< manage_new_object >())
        .def("set_col", &EMAN::EMData::set_col)
        .def("get_attr", &EMAN::EMData::get_attr)
        .def("set_attr", &EMAN::EMData::set_attr)
        .def("get_attr_dict", &EMAN::EMData::get_attr_dict)
        .def("set_attr_dict", &EMAN::EMData::set_attr_dict)
        .def("get_xsize", &EMAN::EMData::get_xsize)
        .def("get_ysize", &EMAN::EMData::get_ysize)
        .def("get_zsize", &EMAN::EMData::get_zsize)
        .def("get_ndim", &EMAN::EMData::get_ndim)
        .def("get_parent", &EMAN::EMData::get_parent, return_value_policy< manage_new_object >())
        .def("set_parent", &EMAN::EMData::set_parent)
        .def("get_value_at", (float (EMAN::EMData::*)(int, int, int) const)&EMAN::EMData::get_value_at)
        .def("get_value_at", (float (EMAN::EMData::*)(int, int) const)&EMAN::EMData::get_value_at)
        .def("get_value_at", (float (EMAN::EMData::*)(size_t) const)&EMAN::EMData::get_value_at)
        .def("sget_value_at", (float (EMAN::EMData::*)(int, int, int) const)&EMAN::EMData::sget_value_at)
        .def("sget_value_at", (float (EMAN::EMData::*)(int, int) const)&EMAN::EMData::sget_value_at)
        .def("sget_value_at", (float (EMAN::EMData::*)(size_t) const)&EMAN::EMData::sget_value_at)
        .def("sget_value_at_interp", (float (EMAN::EMData::*)(float, float) const)&EMAN::EMData::sget_value_at_interp)
        .def("sget_value_at_interp", (float (EMAN::EMData::*)(float, float, float) const)&EMAN::EMData::sget_value_at_interp)
        .def("set_value_at", (void (EMAN::EMData::*)(int, int, int, float) )&EMAN::EMData::set_value_at)
        .def("set_value_at", (void (EMAN::EMData::*)(int, int, float) )&EMAN::EMData::set_value_at)
        .def("is_complex", &EMAN::EMData::is_complex)
        .def("is_real", &EMAN::EMData::is_real)
        .def("set_complex", &EMAN::EMData::set_complex)
        .def("is_complex_x", &EMAN::EMData::is_complex_x)
        .def("set_complex_x", &EMAN::EMData::set_complex_x)
        .def("is_flipped", &EMAN::EMData::is_flipped)
        .def("set_flipped", &EMAN::EMData::set_flipped)
        .def("is_ri", &EMAN::EMData::is_ri)
        .def("set_ri", &EMAN::EMData::set_ri)
        .def("is_fftpadded", &EMAN::EMData::is_fftpadded)
        .def("set_fftpad", &EMAN::EMData::set_fftpad)
        .def("is_fftodd", &EMAN::EMData::is_fftodd)
        .def("set_fftodd", &EMAN::EMData::set_fftodd)
        .def("set_nxc", &EMAN::EMData::set_nxc)
        .def("read_images", &EMAN::EMData::read_images, EMAN_EMData_read_images_overloads_1_3())
        .def("read_images_ext", &EMAN::EMData::read_images_ext, EMAN_EMData_read_images_ext_overloads_3_5())
        .def("onelinenn", &EMAN::EMData::onelinenn)
        .def("nn", &EMAN::EMData::nn)
        .def("symplane0", &EMAN::EMData::symplane0)
        .staticmethod("read_images_ext")
        .staticmethod("read_images")
        .staticmethod("onelinenn")
        .def( self + other< float >() )
        .def( self * other< float >() )
        .def( self - other< float >() )
        .def( other< float >() + self )
        .def( self / other< float >() )
        .def( other< float >() * self )
        .def( other< float >() - self )
        .def( self * self )
        .def( self - self )
        .def( self / self )
        .def( self + self )
        .def( other< float >() / self )
        .def( self += other< float >() )
        .def( self -= other< float >() )
        .def( self *= other< float >() )
        .def( self /= other< float >() )
        .def( self += self )
        .def( self -= self )
        .def( self *= self )
        .def( self /= self )
    );

    enum_< EMAN::EMData::FFTPLACE >("FFTPLACE")
        .value("FFT_IN_PLACE", EMAN::EMData::FFT_IN_PLACE)
        .value("FFT_OUT_OF_PLACE", EMAN::EMData::FFT_OUT_OF_PLACE)
    ;


    enum_< EMAN::EMData::WINDOWPLACE >("WINDOWPLACE")
        .value("WINDOW_OUT_OF_PLACE", EMAN::EMData::WINDOW_OUT_OF_PLACE)
        .value("WINDOW_IN_PLACE", EMAN::EMData::WINDOW_IN_PLACE)
    ;

    delete EMAN_EMData_scope;

}

