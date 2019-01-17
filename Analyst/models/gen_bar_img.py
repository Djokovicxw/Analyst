from pyecharts import Bar, Pie

def gen_bar_img():
    bar = Bar("Last Week")
    bar.add("用户点击量", ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
            [100, 200, 134, 111, 300, 512, 567], mark_line=["average"], mark_point=["max"])
    return bar