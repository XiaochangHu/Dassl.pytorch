from torch.nn import functional as F

from dassl.engine import TRAINER_REGISTRY, TrainerX
from dassl.metrics import compute_accuracy


@TRAINER_REGISTRY.register()
class Vanilla(TrainerX):
    """Vanilla baseline."""

    def forward_backward(self, batch):
        input, label = self.parse_batch_train(batch)
        output = self.model(input)
        loss = F.cross_entropy(output, label)
        self.model_backward_and_update(loss)

        output_dict = {
            'loss': loss.item(),
            'acc': compute_accuracy(output.detach(), label)[0].item(),
            'lr': self.optim.param_groups[0]['lr']
        }

        if (self.batch_idx + 1) == self.num_batches:
            self.update_lr()

        return output_dict

    def parse_batch_train(self, batch):
        input = batch['img']
        label = batch['label']
        input = input.to(self.device)
        label = label.to(self.device)
        return input, label
