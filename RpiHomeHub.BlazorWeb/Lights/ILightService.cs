using RpiHomeHub.BlazorWeb.Colors.Models;
using System.Threading.Tasks;

namespace RpiHomeHub.BlazorWeb.Lights
{
    public interface ILightService<TLightModel> where TLightModel : ILightModel
    {
        Task<TLightModel> GetStatusAsync();
        Task<TLightModel> ToggleAsync();
        Task<TLightModel> TurnOnAsync();
        Task<TLightModel> TurnOffAsync();
        Task<ColorRGB> SetColorAsync(ColorRGB color);
        Task<int> SetBrightnessAsync(int brightness);
    }
}
