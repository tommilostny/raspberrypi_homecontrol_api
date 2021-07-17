using RpiHomeHub.BlazorWeb.Colors.Models;
using System.Threading.Tasks;

namespace RpiHomeHub.BlazorWeb.Lights
{
    public interface ILightService<TLightModel> where TLightModel : ILightModel
    {
        Task<TLightModel> GetStatusAsync();
        Task ToggleAsync(TLightModel light);
        Task TurnOnAsync(TLightModel light);
        Task TurnOffAsync(TLightModel light);
        Task SetColorAsync(ColorRGB color, TLightModel light);
        Task SetBrightnessAsync(int brightness, TLightModel light);
    }
}
