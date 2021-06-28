using System.Threading.Tasks;

namespace RpiHomeHub.BlazorWeb.Lights
{
    public interface ILightService<TLightModel> where TLightModel : ILightModel
    {
        Task<TLightModel> GetStatusAsync();
        Task<TLightModel> ToggleAsync();
        Task<TLightModel> TurnOnAsync();
        Task<TLightModel> TurnOffAsync();
        Task<TLightModel> SetColorAsync(int red, int green, int blue);
        Task<TLightModel> SetBrightnessAsync(int brightness);
    }
}
