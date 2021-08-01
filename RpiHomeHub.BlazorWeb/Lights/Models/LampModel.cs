using RpiHomeHub.BlazorWeb.Colors.Models;
using System.Text.Json.Serialization;

namespace RpiHomeHub.BlazorWeb.Lights.Models
{
    public class LampModel : ILightModel
    {
        public string Power { get; set; }
        
        public ColorRGB Color { get; set; }
        
        public int Brightness { get; set; }

        [JsonIgnore]
        public string Name { get => "Lamp"; }
    }
}
