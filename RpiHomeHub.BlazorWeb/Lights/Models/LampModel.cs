using RpiHomeHub.BlazorWeb.Colors;

namespace RpiHomeHub.BlazorWeb.Lights.Models
{
    public class LampModel : ILightModel
    {
        public string Power { get; set; }
        public ColorRGB Color { get; set; }
        public int Brightness { get; set; }
    }
}
