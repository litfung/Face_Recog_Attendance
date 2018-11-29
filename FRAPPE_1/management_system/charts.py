from .fusioncharts import FusionCharts

def chart(request, total_days, present):
    absent = total_days - present
    # Create an object for the pie3d chart using the FusionCharts class constructor
    string = """{
                "chart":{
                            "caption": "Attendance Pie Chart",
                            "subCaption" : "Present vs Absent",
                            "showValues":"1",
                            "showPercentInTooltip" : "0",
                            "enableMultiSlicing":"1",
                            "theme": "fusion"
                        },
                "data": [{
                            "label": "Present",
                            "value": """ + str(present) + """
                          }, {
                            "label": "Absent",
                            "value": """ + str(absent) + """
                          }]
                }"""
    pie3d = FusionCharts("pie3d", "ex2", "100%", "400", "chart-1", "json",string)
    return pie3d