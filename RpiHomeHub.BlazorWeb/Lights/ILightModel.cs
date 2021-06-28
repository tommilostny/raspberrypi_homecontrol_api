using RpiHomeHub.BlazorWeb.Core;

namespace RpiHomeHub.BlazorWeb.Lights
{
    public interface ILightModel
    {
        string Power { get; set; }
        ColorRGB Color { get; }
        int Brightness { get; set; }
    }
}
