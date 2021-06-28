using System.Threading.Tasks;

namespace RpiHomeHub.BlazorWeb.Lights
{
    public interface ILightService
    {
        Task<ILightModel> GetStatus();
        Task<ILightModel> Toggle();
        Task<ILightModel> TurnOn();
        Task<ILightModel> TurnOff();
        Task<ILightModel> SetColor(int red, int green, int blue);
        Task<ILightModel> SetBrightness(int brightness);
    }
}
