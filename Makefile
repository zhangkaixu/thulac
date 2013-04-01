dst_dir=bin
src_dir=src
cxx=g++ -O3 -I $(src_dir)

all: $(dst_dir)/dat_builder model_c model_w $(dst_dir)/thulac


model_c: $(dst_dir)/train_c $(dst_dir)/predict_c
model_w: $(dst_dir)/train_w $(dst_dir)/predict_w


$(dst_dir)/dat_builder: $(src_dir)/dat_builder.cc $(src_dir)/*.h
	$(cxx) -g -o $(dst_dir)/dat_builder $(src_dir)/dat_builder.cc


$(dst_dir)/train_c: $(src_dir)/train_c.cc $(src_dir)/*.h
	$(cxx) -g -o $(dst_dir)/train_c $(src_dir)/train_c.cc

$(dst_dir)/predict_c: $(src_dir)/predict_c.cc $(src_dir)/*.h
	$(cxx) -g -o $(dst_dir)/predict_c $(src_dir)/predict_c.cc

$(dst_dir)/train_w: $(src_dir)/train_w.cc $(src_dir)/*.h
	$(cxx) $(src_dir)/train_w.cc -o $(dst_dir)/train_w

$(dst_dir)/predict_w: $(src_dir)/predict_w.cc $(src_dir)/*.h
	$(cxx) $(src_dir)/predict_w.cc -o $(dst_dir)/predict_w

$(dst_dir)/thulac: $(src_dir)/thulac.cc $(src_dir)/*.h
	$(cxx) $(src_dir)/thulac.cc -o $(dst_dir)/thulac

clear:
	rm $(dst_dir)/dat_builder -f
	rm $(dst_dir)/train_c -f
	rm $(dst_dir)/predict_c -f
	rm $(dst_dir)/train_w -f
	rm $(dst_dir)/predict_w -f
	rm $(dst_dir)/thulac -f
	
