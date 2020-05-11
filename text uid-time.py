# 弹幕数、用户数-时间曲线图

from pyecharts import options as opts
from pyecharts.charts import Line
from pyecharts.globals import ThemeType

#  timeline_list= [1,2,3,4,5,6,7,8,9,10,11,12]
#  text_list = [5,10,26,30,35,30,20,26,40,46,40,50]
#  uid_list = [8,20,24,36,40,36,40,45,50,53,48,58]

line = (
    Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    .add_xaxis(timeline_list)   # 横轴为时间
    .add_yaxis('弹幕量', text_list)  # 纵轴一弹幕数量
    .add_yaxis('用户', uid_list)      # 纵轴二用户数量
    .set_global_opts(
        title_opts=opts.TitleOpts(title='用户弹幕-时间图',subtitle="折线图"),   # 图表名称
        tooltip_opts=opts.TooltipOpts(trigger='axis', axis_pointer_type='cross'),
        toolbox_opts=opts.ToolboxOpts(is_show=True, orient='vertical', pos_left='right'),
                    )

)
# line.render_notebook()
line.render('弹幕用户-时间图.html')  # 输出为html